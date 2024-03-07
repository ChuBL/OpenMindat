import re
import requests
from pathlib import Path
import sys
import json
from datetime import datetime


class MindatApiTester:
    '''test if api key is valid
    if valid, save it to a file'''
    def __init__(self) -> None:
        pass
    
    def test_api_key_status(self):
        # check if api key is set
        try:
            with open('.api_key', 'r') as f:
                api_key = f.read()
            
            status_code = self.is_api_key_avail(api_key)
            if 200 == status_code:
                self.api_key = api_key
            return status_code
        except FileNotFoundError:
            print("API key not saved.")
            return False
            

    def is_api_key_avail(self, API_KEY):
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
        mat = MindatApiTester()

        status_code = mat.test_api_key_status()

        if 500 == status_code:
            raise Exception("Server Error (500), please try again later.") 
        
        while 200 != mat.is_api_key_avail(self.load_api_key()):
            print('Please input a valid API key. ')
            input_api_key = input("Your API key: ")
            self.set_api_key(input_api_key)
        
        self._api_key = self.load_api_key()

        self.MINDAT_API_URL = "https://api.mindat.org"
        self._headers = {'Authorization': 'Token '+ self._api_key}
        self.params = {'format': 'json'}
        # self.endpoint = "/items/"
        self.data_dir = './mindat_data/'
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def load_api_key(self):
        try:
            with open('.api_key', 'r') as f:
                api_key = f.read()
            return api_key
        except FileNotFoundError:
            return ''
    
    def set_api_key(self, API_KEY):
        '''set api key by saving it to a file'''

        with open('.api_key', 'w') as f:
                f.write(API_KEY)
    
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
         
        
if __name__ == '__main__':
    # test if api key is valid
    ma = MindatApi()