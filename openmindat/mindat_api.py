import os
import re
import sys
import json
import yaml
import requests
import time
from pathlib import Path
from datetime import datetime
from json import JSONDecodeError
from urllib.parse import parse_qsl, urlsplit, urlunsplit
import getpass
import logging

from . import _credentials
from .exceptions import (
    MindatApiKeyError,
    MindatApiKeyNotFoundError,
    MindatApiKeyPromptError,
    MindatRequestError,
    MindatServerError,
)

logger = logging.getLogger("openmindat")

_SERVER_SIDE_NOTE = (
    "This is a problem on the Mindat API server (api.mindat.org), not in openmindat. "
    "Please try again later; if it keeps happening, report it to the Mindat team."
)


def in_notebook():
    '''
        Check if the package is running in notebook, e.g., Jupyter or Colab
        return type: Bool
    '''
    try:
        from IPython import get_ipython
        if 'IPKernelApp' not in get_ipython().config:  # Check if not within an IPython kernel
            return False
    except (ImportError, AttributeError):
        return False
    return True

if in_notebook():
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm

_NO_KEY_HELP = (
    "No Mindat API key found. Set the MINDAT_API_KEY environment variable, or call "
    "openmindat.set_api_key('<your key>', persist=True) once, or run openmindat in an "
    "interactive session to be prompted. Get a key at "
    "https://www.mindat.org/a/how_to_get_my_mindat_api_key"
)

_SOURCE_LABELS = {
    "explicit": "openmindat.set_api_key()",
    "env": "the MINDAT_API_KEY environment variable",
    "config": "the Mindat API key file",
    "legacy": "./.apikey.yaml",
}


def _ask_for_key(prompt):
    '''getpass, but a missing console (scripts, cron, CI) becomes a helpful error instead of EOFError.'''
    try:
        return getpass.getpass(prompt)
    except EOFError as exc:
        raise MindatApiKeyPromptError(_NO_KEY_HELP) from exc


class MindatApiKeyManager:
    '''
        Finds, checks and stores the Mindat API key.

        Sources, in order: openmindat.set_api_key(), the MINDAT_API_KEY environment
        variable, the per-user key file (~/.config/openmindat/credentials.yaml, readable
        only by you) and the legacy ./.apikey.yaml written by openmindat <= 0.1.3, which is
        copied once to the per-user file. Each key is checked with the Mindat API once per
        session.
    '''

    MINDAT_API_URL = "https://api.mindat.org"
    DEFAULT_ENDPOINT = "v1/geomaterials"
    # (connect, read) seconds for the key check.
    STATUS_TIMEOUT = (5, 10)

    def __init__(self, ENDPOINT: str = None):
        self.endpoint = ENDPOINT if ENDPOINT else self.DEFAULT_ENDPOINT

    def inspect_stored_api_key(self):
        '''
            Look for a usable stored key and make it this session's key.
            A key the Mindat API rejects (401/403) is skipped with a warning; a key that
            cannot be checked right now (network error, 429, 5xx) is used anyway.
            Returns True if a usable key was found.
        '''
        for source, key in _credentials.candidates():
            state = self._validate_once(key)
            if state == "invalid":
                _credentials.warn_once(
                    f"invalid:{source}:{key}",
                    f"The Mindat API key from {_SOURCE_LABELS[source]} ({_credentials.mask(key)}) "
                    "was rejected by the Mindat API; trying the next stored key.",
                )
                continue
            if state == "unverified":
                _credentials.warn_once(
                    f"unverified:{key}",
                    f"Could not verify the Mindat API key ({_credentials.mask(key)}) because the "
                    "Mindat API did not answer the check; using it anyway.",
                )
            if source == "legacy":
                self._migrate_legacy_key(key)
            self._activate(key, source)
            return True
        return False

    def get_api_key_input(self):
        api_key = _ask_for_key("Input or get your Mindat API key at https://www.mindat.org/a/how_to_get_my_mindat_api_key: ")

        while False == self.is_valid_key_format(api_key):
            api_key = _ask_for_key("The OpenMindat API key should be a 32-character string. Please re-enter: ")

        state = self._validate_once(api_key)

        while state == "invalid":
            api_key = _ask_for_key("Invalid OpenMindat API key, please try again:")
            state = self._validate_once(api_key)

        if state == "valid":
            self._save_valid_api_key(api_key)
        else:
            # The Mindat API could not check the key right now: use it for this session only.
            _credentials.warn_once(
                f"unverified:{api_key}",
                "Could not verify the Mindat API key because the Mindat API did not answer the "
                "check; using it for this session without saving it.",
            )
            _credentials.set_explicit(api_key)
            self._activate(api_key, "explicit")

    def is_valid_key_format(self, KEY_INPUT):
        """
        Checks if the input string is exactly 32 characters long and consists only of letters and digits.
        
        Args:
        input_string (str): The string to be checked.

        Returns:
        bool: True if the string meets the criteria, False otherwise.
        """
        pattern = r'^[A-Za-z0-9]{32}$'
        return bool(re.match(pattern, KEY_INPUT))
        
    def _save_valid_api_key(self, VALID_KEY):
        _credentials._validation[VALID_KEY] = "valid"
        self._activate(VALID_KEY, "explicit")
        _credentials.set_explicit(VALID_KEY)
        try:
            path = _credentials.write_config_key(VALID_KEY)
        except OSError as exc:
            _credentials.warn_once(
                "save-failed",
                f"Could not save the Mindat API key to {_credentials.config_path()} ({exc}); "
                "it is used for this session only.",
            )
            return True
        _credentials.notice_once(
            f"saved:{path}",
            f"openmindat: saved your Mindat API key to {path} (readable only by you).",
        )
        return True

    def load_api_key(self):
        active = _credentials._session.get("active")
        if active:
            return active
        for _, key in _credentials.candidates():
            return key
        raise MindatApiKeyNotFoundError(_NO_KEY_HELP)

    def reset_api_key(self):
        try:
            del os.environ["MINDAT_API_KEY"]
        except KeyError:
            pass

        try:
            os.remove('./.apikey.yaml')
        except FileNotFoundError:
            pass

        _credentials.remove_config_key()
        _credentials.reset_session()
        return True

    def get_api_key_status(self, api_key: str) -> int:
        try:
            response = requests.get(
                f"{self.MINDAT_API_URL}/{self.endpoint}/",
                headers={'Authorization': f'Token {api_key}'},
                params={'format': 'json', 'page-size': 1},
                timeout=self.STATUS_TIMEOUT
            )
            return response.status_code
        except requests.exceptions.RequestException as e:
            logger.warning("Mindat API key check failed: %s", e)
            return -1

    def _validate_once(self, key):
        '''Check a key with the Mindat API once per session: valid, invalid or unverified.'''
        state = _credentials._validation.get(key)
        if state is None:
            status = self.get_api_key_status(key)
            if status == 200:
                state = "valid"
            elif status in (401, 403):
                state = "invalid"
            else:
                state = "unverified"
            _credentials._validation[key] = state
        return state

    def _activate(self, key, source):
        _credentials._session["active"] = key
        _credentials._session["active_source"] = source
        # openmindat <= 0.1.3 exposed the key in-process this way; kept for existing code.
        os.environ["MINDAT_API_KEY"] = key

    def _migrate_legacy_key(self, key):
        '''Copy a key found in ./.apikey.yaml to the per-user file, once. The old file is left alone.'''
        if _credentials.read_config_key() == key:
            return
        try:
            path = _credentials.write_config_key(key)
        except OSError as exc:
            _credentials.warn_once(
                "migrate-failed",
                f"Could not copy the Mindat API key from ./.apikey.yaml to "
                f"{_credentials.config_path()} ({exc}); still using ./.apikey.yaml.",
            )
            return
        _credentials.notice_once(
            "migrated",
            f"openmindat: copied your Mindat API key from ./.apikey.yaml to {path} (readable only "
            "by you), so it now works from any folder. You may delete ./.apikey.yaml.",
        )


def set_api_key(api_key, persist=False):
    '''
        Use this Mindat API key for the rest of the session.

        Args:
            api_key (str): the 32-character key from https://www.mindat.org/a/how_to_get_my_mindat_api_key
            persist (bool): also save it to the per-user key file (readable only by you),
                so later sessions find it without asking.

        Returns:
            ApiKeyStatus

        Raises:
            MindatApiKeyError: the key is malformed or the Mindat API rejects it.
    '''
    manager = MindatApiKeyManager()
    api_key = (api_key or "").strip()
    if not manager.is_valid_key_format(api_key):
        raise MindatApiKeyError("A Mindat API key is a 32-character string of letters and digits.")
    state = manager._validate_once(api_key)
    if state == "invalid":
        raise MindatApiKeyError(f"The Mindat API rejected the key {_credentials.mask(api_key)}.")
    _credentials.set_explicit(api_key)
    manager._activate(api_key, "explicit")
    if persist:
        path = _credentials.write_config_key(api_key)
        _credentials.notice_once(
            f"saved:{path}", f"openmindat: saved your Mindat API key to {path} (readable only by you)."
        )
    return api_key_status()


def api_key_status():
    '''
        Report which Mindat API key would be used and whether the Mindat API accepts it.
        Never prompts. Returns an ApiKeyStatus (source, state, masked_key, config_path).
    '''
    manager = MindatApiKeyManager()
    config = str(_credentials.config_path())
    if manager.inspect_stored_api_key():
        key = _credentials._session["active"]
        return _credentials.ApiKeyStatus(
            source=_credentials._session["active_source"],
            state=_credentials._validation.get(key, "unverified"),
            masked_key=_credentials.mask(key),
            config_path=config,
        )
    stored = _credentials.candidates()
    if stored:
        source, key = stored[0]
        return _credentials.ApiKeyStatus(source, "invalid", _credentials.mask(key), config)
    return _credentials.ApiKeyStatus(None, "missing", None, config)


class MindatApi:
    '''The main class for openmindat API'''
    # (connect, read) seconds. v0.1.3 had no timeout, so a stalled request could hang forever.
    REQUEST_TIMEOUT = (10, 60)
    # Set to False to get v0.1.3 behaviour for HTTP 4xx: the error body is returned as
    # {"results": [<error>]} instead of raising MindatRequestError.
    RAISE_HTTP_ERRORS = True
    # Smallest page-size used when splitting a page the server cannot answer in time.
    MIN_PAGE_SIZE = 50
    # Longest single wait (seconds) between retries, including a server's Retry-After.
    MAX_RETRY_WAIT = 30
    # Failed attempts allowed at one position in the result set before giving up.
    MAX_FAILURES = 6

    def __init__(self, ENDPOINT: str = None):
        self._api_key = None
        self.endpoint = ENDPOINT or ""
        self._prepare_api_key()
        
        self.MINDAT_API_URL = "https://api.mindat.org"
        self._headers = {'Authorization': 'Token '+ self._api_key}
        self.params = {'format': 'json'}
        self.data_dir = './mindat_data/'
        
        

    def _prepare_api_key(self):
        mam = MindatApiKeyManager(self.endpoint)

        if False == mam.inspect_stored_api_key():
            mam.get_api_key_input()

        self._api_key = mam.load_api_key()
    
    def set_params(self, PARAMS_DICT):
        self.params = PARAMS_DICT

    def set_endpoint(self, ENDPOINT):
        self.endpoint = ENDPOINT
        
    def get_params(self):
        return self.params

    def get_headers(self):
        return self._headers
    
    def get_file_path(self, OUTDIR, FILE_NAME):
        '''
            Reads an End_point
        '''
        file_name = str(FILE_NAME)
        invalid_symbols = re.findall(r"[\\?%*:|\"<>\x7F\x00-\x1F]", file_name)
        
        #input sanitization
        if invalid_symbols:
            raise ValueError(f"Invalid characters in file name: {invalid_symbols}")  
        
        #creating filepath
        if '' == OUTDIR:
            out_dir = Path(self.data_dir)
        else:
            out_dir = Path(OUTDIR)
        
        out_dir.mkdir(parents=True, exist_ok=True)
        return Path(out_dir, file_name.replace('/', '_') + '.json')


    def get_datetime(self):
        # use datetime to get current date and time
        now = datetime.now()
        dt_string = now.strftime("%m%d%Y%H%M%S")
        return dt_string
    
    def get_results(self, URL, json_data, pbar, VERBOSE = 2):
        url = URL        
        
        try:
            response = requests.get(url, headers=self._headers, timeout=self.REQUEST_TIMEOUT)
            new_results = response.json()['results']
            json_data["results"] += new_results
            if VERBOSE == 2:
                pbar.update(len(new_results))
        except TypeError: #special case for locgeoregion2
            json_data["results"]["features"] += new_results["features"]
            if VERBOSE == 2:
                pbar.update(len(new_results))
        #except JSONDecodeError:
        #    raise
            
        return response
    
        
    def get_mindat_json(self, PARAM_DICT, END_POINT, VERBOSE = 2):
        '''
            get all items in a list
            Since this API has a limit of 1500 items per page,
            we need to loop through all pages and save them to a single json file

            Server failures are handled per page: rate limits (429/503) wait and retry,
            gateway timeouts (504/524/read timeout) re-fetch that page as smaller pages,
            and anything unrecoverable raises MindatServerError (a ValueError).
            HTTP 4xx raises MindatRequestError unless RAISE_HTTP_ERRORS is False.
        '''
        params = dict(PARAM_DICT)
        url = self.MINDAT_API_URL + "/" + END_POINT + "/"

        response_json, url_used, params_used = self._fetch_json(url, params, [], VERBOSE)

        if isinstance(response_json, list):
            # The result data is a list instead of a dict; pass it through directly.
            return {"results": response_json}
        if not isinstance(response_json, dict) or "results" not in response_json:
            # The result only has one object; wrap it in a list for consistency.
            return {"results": [response_json]}

        results = list(response_json["results"])
        json_data = {"results": results}

        if not self._is_multipage_query(PARAM_DICT, response_json):
            # A single requested page. If it had to be split, collect the rest of that page.
            requested = self._page_size_of(url, params)
            if requested and self._page_size_of(url_used, params_used) != requested:
                next_url = response_json.get("next")
                while next_url and len(results) < requested:
                    page_json, _, _ = self._fetch_json(next_url, None, results, VERBOSE)
                    results.extend(page_json["results"])
                    next_url = page_json.get("next")
                del results[requested:]
            return json_data

        pbar = tqdm(desc="Fetching data") if VERBOSE == 2 else None
        if pbar is not None:
            pbar.update(len(results))

        next_url = response_json.get("next")
        try:
            while next_url:
                page_json, _, _ = self._fetch_json(next_url, None, results, VERBOSE, pbar)
                new_results = page_json.get("results", []) if isinstance(page_json, dict) else []
                results.extend(new_results)
                if pbar is not None:
                    pbar.update(len(new_results))
                next_url = page_json.get("next") if isinstance(page_json, dict) else None
        finally:
            if pbar is not None:
                pbar.close()

        return json_data

    def _fetch_json(self, url, params, partial_results, VERBOSE=2, pbar=None):
        '''
            Fetch one page and return (json, url, params) for the request that succeeded.
            Retries, waits and page splitting are bounded by MAX_FAILURES.
        '''
        failures = 0
        retried_transient = False
        split_after_server_error = False
        last = None

        while True:
            kind, response, detail = self._send(url, params)

            if kind == "ok":
                return response.json(), url, params

            status = getattr(response, "status_code", None)
            last = (status, detail, response)

            if kind == "client":
                body = self._json_or_none(response)
                if not self.RAISE_HTTP_ERRORS and body is not None:
                    return body, url, params
                raise self._request_error(response, body, partial_results)

            failures += 1
            if failures >= self.MAX_FAILURES:
                raise self._server_error(url, params, last, failures, partial_results)

            if kind == "wait":
                wait = self._retry_after(response, failures)
                self._notice(f"Mindat API asked us to slow down ({detail}); waiting {wait:.0f}s.", VERBOSE, pbar)
                time.sleep(wait)
                continue

            if kind in ("transient", "server") and not retried_transient:
                retried_transient = True
                wait = min(2 ** failures, self.MAX_RETRY_WAIT)
                self._notice(f"Mindat API error ({detail}); retrying in {wait:.0f}s.", VERBOSE, pbar)
                time.sleep(wait)
                continue

            if kind == "server":
                if split_after_server_error:
                    raise self._server_error(url, params, last, failures, partial_results, size_ruled_out=True)
                split_after_server_error = True

            # The page is probably too heavy for the server: ask for the same records in smaller pages.
            smaller = self._smaller_page(url, params)
            if smaller is None:
                wait = min(2 ** failures, self.MAX_RETRY_WAIT)
                time.sleep(wait)
                continue
            url, params = smaller
            self._notice(
                f"Mindat API could not answer in time ({detail}); retrying with page size "
                f"{self._page_size_of(url, params)}.", VERBOSE, pbar)

    def _send(self, url, params):
        '''Send one GET and classify the outcome: ok, client, wait, heavy, server or transient.'''
        connection_error = getattr(requests.exceptions, "ConnectionError", ())
        try:
            response = requests.get(url, params=params, headers=self._headers, timeout=self.REQUEST_TIMEOUT)
        except requests.exceptions.Timeout as e:
            if connection_error and isinstance(e, connection_error):  # connect timeout
                return "transient", None, "connection timed out"
            return "heavy", None, "read timed out"
        except connection_error as e:
            return "transient", None, f"connection error: {e}"

        if len(response.url) > 4097:
            raise ValueError("Search query to big, reduce the size of the search and try again.")

        status = response.status_code
        label = f"HTTP {status} {response.reason}".strip()
        if status == 200:
            if self._json_or_none(response) is None:
                return "transient", response, "HTTP 200 with a non-JSON body"
            return "ok", response, label
        if status in (429, 503):
            return "wait", response, label
        if status in (408, 504, 524):
            return "heavy", response, label
        if 400 <= status < 500:
            return "client", response, label
        return "server", response, label

    @staticmethod
    def _json_or_none(response):
        try:
            return response.json()
        except ValueError:
            return None

    def _retry_after(self, response, failures):
        value = getattr(response, "headers", {}).get("Retry-After")
        try:
            wait = float(value)
        except (TypeError, ValueError):
            wait = 2 ** failures
        return min(max(wait, 1), self.MAX_RETRY_WAIT)

    @staticmethod
    def _query_of(url, params):
        query = dict(parse_qsl(urlsplit(url).query))
        query.update(params or {})
        return query

    def _page_size_of(self, url, params):
        try:
            return int(self._query_of(url, params)["page-size"])
        except (KeyError, TypeError, ValueError):
            return None

    def _smaller_page(self, url, params):
        '''
            Return (url, params) asking for the records from the same offset with a smaller
            page-size, or None if the page cannot be split.
        '''
        query = self._query_of(url, params)
        size = self._page_size_of(url, params)
        if size is None:
            return None
        try:
            page = int(query.get("page", 1))
        except ValueError:
            return None
        offset = (page - 1) * size
        for candidate in range(size // 2, self.MIN_PAGE_SIZE - 1, -1):
            if offset % candidate == 0:
                break
        else:
            return None
        query["page-size"] = candidate
        new_page = offset // candidate + 1
        if new_page != 1 or "page" in query:
            query["page"] = new_page
        parts = urlsplit(url)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", "")), query

    def _notice(self, message, VERBOSE, pbar=None):
        logger.info(message)
        if VERBOSE:
            write = getattr(pbar, "write", None) if pbar is not None else None
            (write or print)(message)

    def _request_error(self, response, body, partial_results):
        status = response.status_code
        detail = ""
        if isinstance(body, dict):
            detail = body.get("error") or body.get("detail") or ""
        detail = str(detail or response.reason or "").strip()
        hint = ""
        if status in (401, 403):
            hint = " Check that your Mindat API key is valid."
        elif status == 404:
            hint = " The requested record or endpoint does not exist."
        message = (
            f"The Mindat API rejected the request (HTTP {status} {response.reason}): {detail}.{hint}\n"
            f"Request: {response.url}"
        )
        return MindatRequestError(message, status_code=status, url=response.url, payload=body,
                                  partial_results=list(partial_results))

    def _server_error(self, url, params, last, attempts, partial_results, size_ruled_out=False):
        status, detail, response = last
        request_url = getattr(response, "url", None) or url
        if size_ruled_out:
            what = (f"The Mindat API server returned {detail} even for smaller pages, "
                    f"so the query size is not the cause.")
        elif status == 429 or status == 503:
            what = f"The Mindat API server is rate-limiting or unavailable ({detail}) after {attempts} attempts."
        else:
            what = f"The Mindat API server failed to answer ({detail}) after {attempts} attempts."
        kept = f" {len(partial_results)} records downloaded before the failure are in .partial_results." \
            if partial_results else ""
        message = f"{what} {_SERVER_SIDE_NOTE}{kept}\nRequest: {request_url}"
        return MindatServerError(message, status_code=status, url=request_url,
                                 payload=self._json_or_none(response) if response is not None else None,
                                 partial_results=list(partial_results))

    def _is_multipage_query(self, PARAM, RAW_JSON):
        if 'page' in PARAM:
            return False
        
        raw_json = RAW_JSON
        try:
            result_data = raw_json["results"]
        except:
            return False

        return True

    def download_mindat_json(self, QUERY_DICT, END_POINT, OUTDIR = '', FILE_NAME = '', VERBOSE = 2):
        '''
            get all items in a list
            Since this API has a limit of 1000 items per page,
            we need to loop through all pages and save them to a single json file
        '''
        # get the json data
        json_data = self.get_mindat_json(QUERY_DICT, END_POINT, VERBOSE)

        # The default output name is same as the endpoint
        file_name = FILE_NAME if FILE_NAME else END_POINT   

        # Getting the directory for the output file
        file_path = self.get_file_path(OUTDIR, file_name)

        # Create and write the json data to the file
        with open(file_path, 'w') as f:
            json.dump(json_data, f, indent=4)   

        if VERBOSE > 0:
            print("Successfully saved " + str(len(json_data['results'])) + " entries to " + str(file_path.resolve()))
        
if __name__ == '__main__':
    # test if api key is valid
    ma = MindatApi()
