import re
import requests
from pathlib import Path
import sys
import json
from datetime import datetime
import getpass
import yaml
import os


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
        # self.endpoint = "/items/"
        self.data_dir = './mindat_data/'
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

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
            return Path(self.data_dir, file_name.replace('/', '_') + '.json')
        else:
            return Path(OUTDIR, file_name.replace('/', '_') + '.json')
    
    def get_mindat_search(self, QUERY_DICT, END_POINT, OUTDIR = '', FILE_NAME = ''):
        params = QUERY_DICT
    
        end_point = END_POINT
        file_name = FILE_NAME if FILE_NAME else END_POINT        
        
        file_path = self.get_file_path(OUTDIR, file_name)

        with open(file_path, 'w') as f:

            params = QUERY_DICT

            response = requests.get(self.MINDAT_API_URL+ "/" + end_point + "/",
                            params=params,
                            headers=self._headers)
            
            try:
                result_data = response.json()
            except:
                print("Error: " + str(response.json()))
                return

            json_data = {"results": result_data}

            json.dump(json_data, f, indent=4)

        print("Successfully saved " + str(len(json_data['results'])) + " entries to " + str(file_path.resolve()))


    def print_the_result(self, JSONFILE, FILENAME):
        print("Successfully retrieved", len(JSONFILE['results']), "items in", FILENAME, '. ')


    def get_datetime(self):
        # use datetime to get current date and time
        now = datetime.now()
        dt_string = now.strftime("%m%d%Y%H%M%S")
        return dt_string        

    def get_mindat_list(self, QUERY_DICT, END_POINT, OUTDIR = '', FILE_NAME = ''):
        '''
            get all items in a list
            Since this API has a limit of 1500 items per page,
            we need to loop through all pages and save them to a single json file
        '''

        end_point = END_POINT
        file_name = FILE_NAME if FILE_NAME else END_POINT        
        
        file_path = self.get_file_path(OUTDIR, file_name)

        with open(file_path, 'w') as f:

            params = QUERY_DICT

            if len(params) <= 2 and 'format' in params and 'page_size' in params:
                confirm = input("The query dict only has 'format' and 'page_size' keys. Do you confirm this query? (y/n): ")
                if confirm.lower() != 'y':
                    sys.exit("Query not confirmed. Exiting...")

            response = requests.get(self.MINDAT_API_URL+ "/" + end_point + "/",
                            params=params,
                            headers=self._headers)
            
        
            try:
                result_data = response.json()["results"]
            except:
                print("Error: " + str(response.json()))
                return
            
            json_data = {"results": result_data}

            while True:
                try:
                    next_url = response.json()["next"]
                    response = requests.get(next_url, headers=self._headers)
                    json_data["results"] += response.json()['results']

                except requests.exceptions.MissingSchema as e:
                    # This error indicates the `next_url` is none
                    # i.e., we've reached the end of the results
                    break

            json.dump(json_data, f, indent=4)            
        print("Successfully saved " + str(len(json_data['results'])) + " entries to " + str(file_path.resolve()))
        
    def get_mindat_item(self, QUERY_DICT, END_POINT, OUTDIR = '', FILE_NAME = ''):
        '''
            return one item.
        '''
        
        end_point = END_POINT
        file_name = FILE_NAME if FILE_NAME else END_POINT  
        
        file_path = self.get_file_path(OUTDIR, file_name)
        
        with open(file_path, 'w') as f:

            params = QUERY_DICT

            if len(params) <= 2 and 'format' in params and 'page_size' in params:
                confirm = input("The query dict only has 'format' and 'page_size' keys. Do you confirm this query? (y/n): ")
                if confirm.lower() != 'y':
                    sys.exit("Query not confirmed. Exiting...")

            response = requests.get(self.MINDAT_API_URL+ "/" + end_point + "/",
                            params=params,
                            headers=self._headers)
            
            try:
                result_data = response.json()
            except:
                print("Error: " + str(response.json()))
                return
            
            json_data = {"results": result_data}

            json.dump(json_data, f, indent=4)
        print("Successfully saved item to " + str(file_path.resolve()))
        
    def get_mindat_list_object(self, QUERY_DICT, END_POINT):
        '''
            get all items in a list and returns it to a list of dictionaries
            Since this API has a limit of 1500 items per page,
            we need to loop through all pages and save them to a single json file
        '''

        end_point = END_POINT

        params = QUERY_DICT

        if len(params) <= 2 and 'format' in params and 'page_size' in params:
            confirm = input("The query dict only has 'format' and 'page_size' keys. Do you confirm this query? (y/n): ")
            if confirm.lower() != 'y':
                sys.exit("Query not confirmed. Exiting...")

        response = requests.get(self.MINDAT_API_URL+ "/" + end_point + "/",
                        params=params,
                        headers=self._headers)
            
        
        try:
            result_data = response.json()["results"]
        except:
            print("Error: " + str(response.json()))
            return
            
        json_data = result_data

        while True:
            try:
                next_url = response.json()["next"]
                response = requests.get(next_url, headers=self._headers)
                json_data += response.json()['results']

            except requests.exceptions.MissingSchema as e:
                # This error indicates the `next_url` is none
                # i.e., we've reached the end of the results
                break
        
        return json_data
    
    def get_mindat_dict(self, QUERY_DICT, END_POINT):
        '''
            return one item to an object as a dictionary.
        '''
        end_point = END_POINT
        params = QUERY_DICT

        if len(params) <= 2 and 'format' in params and 'page_size' in params:
            confirm = input("The query dict only has 'format' and 'page_size' keys. Do you confirm this query? (y/n): ")
            if confirm.lower() != 'y':
                sys.exit("Query not confirmed. Exiting...")

        response = requests.get(self.MINDAT_API_URL+ "/" + end_point + "/",
                        params=params,
                        headers=self._headers)
        
        try:
            result_data = response.json()
        except:
            print("Error: " + str(response.json()))
            return
            
        json_data = result_data
        
        return json_data
        
if __name__ == '__main__':
    # test if api key is valid
    ma = MindatApi()