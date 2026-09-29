"""Shared machinery for the retriever classes.

Every retriever used to carry its own copy of these methods. They live here now;
behaviour, method names and parameter names are unchanged (see
tests/refactor/test_backward_compat.py).

Only methods every retriever already had are defined on the classes, and helpers are
module-level functions, so ``available_methods()`` and ``dir()`` list exactly what they
listed before.
"""

from . import mindat_api
from .exceptions import MindatRequestError


def _as_int(value, name):
    """Coerce an integer-like argument (bool, int, "3", 3.0) or raise ValueError."""
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        raise ValueError(f"{name} must be an integer, got {value!r}")
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be an integer, got {value!r}") from None


def _with_sub_listing_hint(retriever, exc):
    """Add the retriever's _SUB_LISTING_HINT to a 404 caused by querying without a sub-listing."""
    hint = retriever._SUB_LISTING_HINT
    if hint and exc.status_code == 404 and getattr(retriever, "sub_endpoint", None) == "":
        return MindatRequestError(
            f"{hint}\n{exc}", status_code=exc.status_code, url=exc.url,
            payload=exc.payload, partial_results=exc.partial_results,
        )
    return None


def _request_endpoint(retriever):
    """The endpoint a query is sent to, following the retriever's _ENDPOINT_STYLE."""
    style = retriever._ENDPOINT_STYLE
    if style == "plain":
        return retriever.end_point
    if style == "join":
        # With no id this yields a trailing slash (e.g. "v1/locality-age/"); kept as-is.
        return f"{retriever.end_point}/{retriever.sub_endpoint}"
    if style == "join_if_sub":
        if retriever.sub_endpoint != "":
            return f"{retriever.BASE_ENDPOINT}/{retriever.sub_endpoint}"
        return retriever.end_point
    if style == "join_varieties":
        sub_endpoint = retriever.sub_endpoint
        if retriever.variety:
            sub_endpoint = f"{sub_endpoint}/varieties"
        return f"{retriever.end_point}/{sub_endpoint}"
    raise AssertionError(f"unknown _ENDPOINT_STYLE {style!r}")


class _BaseRetriever:
    """Base for all retrievers: query state, paging size, verbosity, execution."""

    BASE_ENDPOINT = ""
    # How the request endpoint is built: plain | join | join_if_sub | join_varieties
    _ENDPOINT_STYLE = "plain"
    # Whether the retriever keeps a `sub_endpoint` attribute (ids, sub-listings).
    _HAS_SUB_ENDPOINT = False
    # Extra message for the 404 the Mindat API returns when no sub-listing/id was chosen.
    _SUB_LISTING_HINT = None

    def __init__(self):
        self.end_point = self.BASE_ENDPOINT
        self.verbose_flag = 2
        if self._HAS_SUB_ENDPOINT:
            self.sub_endpoint = ''
        self._params = {}
        self._init_params()

    def _init_params(self):
        self.end_point = self.BASE_ENDPOINT
        self.verbose_flag = 2
        if self._HAS_SUB_ENDPOINT:
            self.sub_endpoint = ''
        self._params.clear()
        self._params = {'format': 'json'}
        self.page_size(1500)

    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The retriever object.

        Example:
            >>> r.page_size(50).saveto()
        '''
        self._params.update({
            'page-size': PAGE_SIZE
        })
        return self

    def verbose(self, FLAG):
        '''
        Determines the verbose mode of the query.

        Args:
            FLAG (int): 0 = silent, 1 = save notifications, 2 (default) = progress bar

        Returns:
            self: The retriever object.

        Example:
            >>> r.verbose(0).saveto("/path/to/directory")
        '''
        if isinstance(FLAG, int):
            flag = FLAG
        else:
            # ValueError (not TypeError) is what every release has raised here.
            raise ValueError(f"Possible Invalid ENTRYTYPE: {FLAG}\nPlease retry.")  # noqa: TRY004

        self.verbose_flag = flag
        return self

    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
        Executes the query and saves the results to a specified directory.

        Args:
            OUTDIR (str): The directory where the results are saved. Defaults to ./mindat_data/.
            FILE_NAME (str): Optional file name; defaults to the endpoint name.

        Returns:
            None

        Example:
            >>> r.saveto("/path/to/directory", "my_results")
        '''
        params = self._params
        end_point = _request_endpoint(self)
        outdir = OUTDIR
        file_name = FILE_NAME
        verbose = self.verbose_flag

        ma = mindat_api.MindatApi()
        try:
            ma.download_mindat_json(params, end_point, outdir, file_name, verbose)
        except MindatRequestError as exc:
            hinted = _with_sub_listing_hint(self, exc)
            if hinted is None:
                raise
            raise hinted from exc

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()

    def save(self, FILE_NAME = ''):
        '''
        Executes the query and saves the results to ./mindat_data/.

        Args:
            FILE_NAME (str): Optional file name; defaults to the endpoint name.

        Returns:
            None

        Example:
            >>> r.save()
        '''
        file_name = FILE_NAME
        self.saveto('', file_name)

    def get_dict(self):
        '''
        Executes the query and returns the results as a dictionary.

        Returns:
            dict: {"results": [...]}

        Example:
            >>> results = r.get_dict()
        '''
        params = self._params
        end_point = _request_endpoint(self)
        verbose = self.verbose_flag

        ma = mindat_api.MindatApi()
        try:
            results = ma.get_mindat_json(params, end_point, verbose)
        except MindatRequestError as exc:
            hinted = _with_sub_listing_hint(self, exc)
            if hinted is None:
                raise
            raise hinted from exc

        self._init_params()
        return results

    def available_methods(self):
        '''
        Prints the available methods of the class.

        Example:
            >>> r.available_methods()
        '''
        methods = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        print("Available methods:", methods)

    def __getattr__(self, name):
        '''
        Custom attribute access method to handle mistyped method names.
        '''
        methods = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        if name not in methods:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}', \nAvailable methods: {methods}")
        return object.__getattribute__(self, name)


class _PagedRetriever(_BaseRetriever):
    """Retrievers over paginated list endpoints (adds page())."""

    def page(self, PAGE):
        '''
        Sets the page of results to return.

        Args:
            PAGE (int): The page number.

        Returns:
            self: The retriever object.

        Example:
            >>> r.page(2).save()
        '''
        self._params.update({
            "page": PAGE
        })
        return self


class _IdRetriever(_BaseRetriever):
    """Retrievers addressing one record (or sub-listing) below BASE_ENDPOINT (adds id())."""

    _ENDPOINT_STYLE = "join"
    _HAS_SUB_ENDPOINT = True

    def id(self, ID):
        '''
        Sets the id of the record to return.

        Args:
            ID (int): The record id.

        Returns:
            self: The retriever object.

        Example:
            >>> r.id(2).saveto("/path/to/directory")
        '''
        try:
            ID = int(ID)
        except ValueError:
            raise ValueError("Invalid input. ID must be a valid integer.")

        id = str(ID)
        self.sub_endpoint = id
        return self
