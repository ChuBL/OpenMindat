import os
import re
import sys
import json
import yaml
import requests
from pathlib import Path
from datetime import datetime
import getpass


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

class MindatApiKeyManeger:
    def __init__(self):
        pass

    def inspect_stored_api_key(self):
        try:
            env_api_key = os.environ["MINDAT_API_KEY"]
            status_code = self.get_api_key_status(env_api_key)
            if 200 == status_code:
                self._save_valid_api_key(env_api_key)
                return True
        except KeyError:
            pass

        try:
            with open('./.apikey.yaml', 'r') as f:
                yaml_api_key = yaml.safe_load(f)['api_key']
            
            status_code = self.get_api_key_status(yaml_api_key)
            if 200 == status_code:
                self._save_valid_api_key(yaml_api_key)
                return True
        except FileNotFoundError:
            pass

        return False
    
    def get_api_key_input(self):
        api_key = getpass.getpass("Input or get your Mindat API key at https://www.mindat.org/a/how_to_get_my_mindat_api_key: ")

        while False == self.is_valid_key_format(api_key):
            api_key = getpass.getpass("The OpenMindat API key should be a 32-character string. Please re-enter: ")

        status_code = self.get_api_key_status(api_key)

        while 401 == status_code:
            api_key = getpass.getpass("Invalid OpenMindat API key, please try again:")
            status_code = self.get_api_key_status(api_key)

        if 200 == status_code:
            self._save_valid_api_key(api_key)
        else:
            raise ValueError("Mindat server error, please try again later.")
        
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
        os.environ["MINDAT_API_KEY"] = VALID_KEY

        with open('./.apikey.yaml', 'w') as f:
            yaml.dump({'api_key': VALID_KEY}, f)
        
        return True
    
    def load_api_key(self):
        if os.environ.get("MINDAT_API_KEY"):
            api_key = os.environ.get("MINDAT_API_KEY")
        else:
            with open('./.apikey.yaml', 'r') as f:
                api_key = yaml.safe_load(f)['api_key']
        return api_key
    
    def reset_api_key(self):
        try:
            del os.environ["MINDAT_API_KEY"]
        except KeyError:
            pass
        
        try:
            os.remove('./.apikey.yaml')
        except FileNotFoundError:
            pass
        return True

    def get_api_key_status(self, API_KEY):
        # test if api key is valid
        test_api_key = API_KEY
        MINDAT_API_URL = "https://api.mindat.org"
        test_headers = {'Authorization': 'Token '+ test_api_key}
        test_params = {'format': 'json'}
        test_response = requests.get(MINDAT_API_URL+"/geomaterials/",
                                params=test_params,
                                headers=test_headers)
        
        return test_response.status_code


class MindatApi:
    '''The main class for openmindat API'''
    def __init__(self):
        self._api_key = None
        self._prepare_api_key()

        self.MINDAT_API_URL = "https://api.mindat.org"
        self._headers = {'Authorization': 'Token '+ self._api_key}
        self.params = {'format': 'json'}
        self.data_dir = './mindat_data/'

    def _prepare_api_key(self):
        mam = MindatApiKeyManeger()

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
    
        
    def get_mindat_json(self, PARAM_DICT, END_POINT):
        '''
            get all items in a list
            Since this API has a limit of 1500 items per page,
            we need to loop through all pages and save them to a single json file
        '''
        params = PARAM_DICT
        end_point = END_POINT

        # Retrieve the first page of data
        response = requests.get(self.MINDAT_API_URL+ "/" + end_point + "/",
                        params=params,
                        headers=self._headers)
        try:
            response_json = response.json()
            result_data = response_json["results"]
        except KeyError:
            # This error indicates the result only has one page
            # We will convert the result data into a list for consistency
            result_data = [response_json]
        except TypeError:
            # This error indicates the result data is a list instead of a dict
            # We will pass the response result directly
            result_data = response_json
        except:
            raise ValueError(str(response.reason))
        
        # Format the obtained data in a JSON dict
        json_data = {"results": result_data}

        # Check if the query involves multiple pages
        multipage_flag = self._is_multipage_query(params, response.json())
        
        if True == multipage_flag:
            # Create the progress bar
            total_item = response.json().get("count", None)
            item_per_request = len(response.json()["results"])
            pbar = tqdm(total=total_item, desc="Fetching data") if total_item is not None else tqdm(desc="Fetching data")
            pbar.update(item_per_request)

            # Try if multipage download is needed
            while True:
                try:
                    next_url = response.json()["next"]
                    response = requests.get(next_url, headers=self._headers)
                    new_results = response.json()['results']
                    json_data["results"] += new_results
                    pbar.update(len(new_results))
                except requests.exceptions.MissingSchema:
                    # This error indicates the `next_url` is none
                    # i.e., No more pages to fetch
                    break

            # Close the progress bar
            pbar.close()
            
        return json_data
    
    def _is_multipage_query(self, PARAM, RAW_JSON):
        if 'page' in PARAM:
            return False
        
        raw_json = RAW_JSON
        try:
            result_data = raw_json["results"]
        except:
            return False

        return True

    def download_mindat_json(self, QUERY_DICT, END_POINT, OUTDIR = '', FILE_NAME = ''):
        '''
            get all items in a list
            Since this API has a limit of 1000 items per page,
            we need to loop through all pages and save them to a single json file
        '''
        # get the json data
        json_data = self.get_mindat_json(QUERY_DICT, END_POINT)

        # The default output name is same as the endpoint
        file_name = FILE_NAME if FILE_NAME else END_POINT   

        # Getting the directory for the output file
        file_path = self.get_file_path(OUTDIR, file_name)

        # Create and write the json data to the file
        with open(file_path, 'w') as f:
            json.dump(json_data, f, indent=4)   

        print("Successfully saved " + str(len(json_data['results'])) + " entries to " + str(file_path.resolve()))
        
if __name__ == '__main__':
    # test if api key is valid
    ma = MindatApi()