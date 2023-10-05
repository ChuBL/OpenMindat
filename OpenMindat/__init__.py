from pathlib import Path
import os
import sys
import json
import re
import pprint
import requests


def set_api_key(API_KEY):
    # set api key and save it to a file
    mat = MindatApiTester()

    if mat.test_api_key(API_KEY):
        mat.api_key = API_KEY
        with open('cached_api_key', 'w') as f:
            f.write(API_KEY)
        print("API key is saved. ")
    else:
        print("API key is invalid. Please check your API key. ")

class MindatApiTester:
    def __init__(self) -> None:
        self.api_key = None
    
    def has_api_key(self):
        # check if api key is set
        try:
            with open('cached_api_key', 'r') as f:
                api_key = f.read()
            if self.test_api_key(api_key):
                self.api_key = api_key
                return True
            else:
                print("Cached API key is invalid.")
                return False
        except FileNotFoundError:
            print("API key not set.")
            return False
            

    def test_api_key(self, API_KEY):
        # test if api key is valid
        test_api_key = API_KEY
        MINDAT_API_URL = "https://api.mindat.org"
        test_headers = {'Authorization': 'Token '+ test_api_key}
        test_params = {'format': 'json'}
        test_response = requests.get(MINDAT_API_URL+"/geomaterials/",
                                params=test_params,
                                headers=test_headers)
        if test_response.status_code == 200:
            return True
        else:
            return False

class MindatApi:
    def __init__(self):
        mat = MindatApiTester()
        if False == mat.has_api_key():
            print("Please set your API key using this function: \n\
set_api_key('Your_API_Key'). ")
            return
        else:
            self._api_key = self.load_api_key()
        
        print('successfully loaded API key. ')
        
        self.MINDAT_API_URL = "https://api.mindat.org"
        self._headers = {'Authorization': 'Token '+ self._api_key}
        self.params = {'format': 'json'}
        self.endpoint = "/items/"
        self.data_dir = './mindat_data/'
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def load_api_key(self):
        with open('cached_api_key', 'r') as f:
            api_key = f.read()
        return api_key
    


    def set_params(self, PARAMS_DICT):
        self.params = PARAMS_DICT

    def set_endpoint(self, ENDPOINT):
        self.endpoint = ENDPOINT
        
    def get_params(self):
        return self.params

    def get_headers(self):
        return self._headers
    
    def get_items(self, PARAMS_DICT = {}, FILENAME = 'mindat_items'):
        if {} == PARAMS_DICT:
            params = self.params
        else:
            params = PARAMS_DICT
        print("Retrieving items with params:")
        pprint.pprint(params)

        response = requests.get(self.MINDAT_API_URL+"/items/",
                                params=params,
                                headers=self._headers)

        json_file = response.json()
        if 'mindat_items' == FILENAME:
            export_path = self.data_dir + 'mindat_items.json'
        else:
            export_path = self.data_dir + FILENAME + '.json'
        
        with open(export_path, 'w') as f:
            json.dump(json_file, f, indent=4)
        
        self.print_the_result(json_file, FILENAME)

    def print_the_result(self, JSONFILE, FILENAME):
        print("Successfully retrieved", len(JSONFILE['results']), "items in", FILENAME, '. ')

    

    def get_all_items(self):
        # https://api.mindat.org/items/?format=json
        # return all mindat items (minerals, varieties, groups, synonyms, rocks, etc.),
        # unfiltered, paginated
        params = {'format': 'json',
                'page_size': '20'}
        response = requests.get(self.MINDAT_API_URL+"/items/",
                                params=params,
                                headers=self._headers, )
        json_file = response.json()
        saving_path = self.data_dir + 'mindat_items.json'
        with open(saving_path, 'w') as f:
            json.dump(json_file, f, indent=4)

    def get_select_fields_items(self, FILEDS_STR = 'id,name,dispformulasimple',\
                PAGE_SIZE = '100'):
        # https://api.mindat.org/items/?fields=id,name,dispformulasimple&page_size=100
        # display only selected fields.
        # selecting only necessary fields slightly reduces db queries size so its appreciated
        # customize page_size to 100 items per page
        params = {'fields': FILEDS_STR,
                'page_size': PAGE_SIZE,
                'format': 'json'}

        response = requests.get(self.MINDAT_API_URL+"/items/",
                        params=params,
                        headers=self._headers)

        json_file = response.json()
        field_sequence = re.sub(r'\,','_',FILEDS_STR)
        saving_path = self.data_dir + 'mindat_items_with_fields_' + field_sequence + '.json'
        with open(saving_path, 'w') as f:
            json.dump(json_file, f, indent=4)

    def get_omit_fields_items(self, OMIT_STR = 'id,name,dispformulasimple'):
        # https://api.mindat.org/items/?omit=id,name,dispformulasimple
        # exclude fields from display
        params = {'omit': OMIT_STR,
                'format': 'json'}

        response = requests.get(self.MINDAT_API_URL+"/items/",
                        params=params,
                        headers=self._headers)

        json_file = response.json()
        omit_sequence = re.sub(r'\,','_',OMIT_STR)
        saving_path = self.data_dir + 'mindat_items_omit_fields_' + omit_sequence + '.json'
        with open(saving_path, 'w') as f:
            json.dump(json_file, f, indent=4)

    def get_filtered_items(self, FILTERS_DICT = {'density__to': '3',
          'crystal_system': 'Triclinic',
          'color': 'red',
          'ima': 1,          # show only minerals approved by ima
          'format': 'json'}):
        # for filters reference on this endpoint see generated documentation:
        # https://api.mindat.org/schema/redoc/#tag/items/operation/items_list
        
        # filters on minerals, examples
        # https://api.mindat.org/items/?density__to=3&crystal_system=Triclinic&color=red&ima=1
        params = FILTERS_DICT
        response = requests.get(self.MINDAT_API_URL+"/items/",
                        params=params,
                        headers=self._headers)

        json_file = response.json()
        saving_path = self.data_dir + 'mindat_items_filtered.json'
        with open(saving_path, 'w') as f:
            json.dump(json_file, f, indent=4)

    def get_datetime(self):
        # use datetime to get current date and time
        now = datetime.now()
        dt_string = now.strftime("%m%d%Y%H%M%S")
        return dt_string

    def get_ima_items(self):
        '''
            get all minerals approved by ima.
            Since this API has a limit of 1000 items per page,
            we need to loop through all pages and save them to a single json file
        '''
        # omit_str = '''updttime,varietyof,synid,polytypeof,groupid,
        #     entrytype,entrytype_text,description_short,impurities
        #     '''
        ima_path = Path(self.data_dir, 'raw_data')
        ima_path.mkdir(parents=True, exist_ok=True)
        date = self.get_datetime()
        print("Retrieving Mindat data for IMA approved minerals. This may take a while... ")
        file_path = Path(ima_path, 'mindat_items_IMA_' + date + '.json')
        with open(file_path, 'w') as f:

            params = {
                #'omit': omit_str,
                #'fields': "id,name,elements",
                "ima_status": [
                        "APPROVED"
                    ],
                'format': 'json'
            }

            response = requests.get(self.MINDAT_API_URL+"/geomaterials/",
                            params=params,
                            headers=self._headers)

            result_data = response.json()["results"]
            json_data = {"results": result_data}

            while True:
                try:
                    next_url = response.json()["next"]
                    response = requests.get(next_url, headers=self._headers)
                    json_data["results"] += response.json()['results']

                except requests.exceptions.MissingSchema as e:
                    # This error indicates the `next_url` is none
                    break
            # last_count = self.ima_last_count_check(ima_path)
            # if last_count > len(json_all['results']):
            #     print('IMA approved minerals retrieving failed. Exiting...')
            #     return
            json.dump(json_data, f, indent=4)
        print("Successfully saved " + str(len(json_data['results'])) + " entries to " + str(file_path))


if __name__ == "__main__":
    ma = MindatApi()
    # assert(ma._test_api_key('194b8286f1eceab9c9591ba748df6652') == True)