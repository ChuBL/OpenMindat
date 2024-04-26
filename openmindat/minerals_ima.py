from . import mindat_api
from datetime import datetime

class MineralsIMARetriever:
    '''
    A class for querying mineral data from the Mindat API. It supports various query parameters such as mineral IDs, IMA status, fields selection, and pagination. The class enables method chaining for building complex queries and provides functionalities to save the queried data either to a specified directory or the current directory.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/minerals_ima

    Usage:
        >>> mir = MineralsIMARetriever()
        >>> mir.ima(1).fields("id,name,ima_formula").saveto("/path/to/directory")

    Press q to quit.
    '''
    def __init__(self):
        self.end_point = 'minerals_ima'
        self._params = {}
        self._init_params()

    def _init_params(self):
        self.end_point = 'minerals_ima'
        self._params.clear()
        self._params = {'format': 'json'}
        self.page_size(1500)

    def expand(self, EXPAND_FIELDS):
        '''
        Expand the query to include related minerals and select specific fields to expand.

        Args:
            EXPAND_FIELDS(list[str] or str): The fields to expand. Valid options are:
                - "description"
                - "type_localities"
                - "locality"
                - "relations"
                - "minstats"
                - "~all" (expand all fields)
                - "*" (expand all fields)

        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.expand(["description", "type_localities"])
            >>> mir.saveto()
        '''

        valid_options = ["description", "type_localities", "locality", "relations", "minstats", "~all", "*"]

        if isinstance(EXPAND_FIELDS, str):
            EXPAND_FIELDS = [EXPAND_FIELDS]

        invalid_options = [field for field in EXPAND_FIELDS if field not in valid_options]

        if invalid_options:
            raise ValueError(f"Invalid EXPAND_FIELDS: {', '.join(invalid_options)}\nEXPAND_FIELDS must be one or more of the following: {', '.join(valid_options)}")

        expand_fields = EXPAND_FIELDS
        self._params.update({
            'expand': expand_fields
        })

        return self
    
    def fields(self, FIELDS):
        '''
        Specify the selected fields to be retrieved for each geomaterial.
        Please check the API documentation for the list of available fields.
        https://api.mindat.org/schema/redoc/#tag/minerals_ima/operation/minerals_ima_list

        Args:
            FIELDS (str): The selected fields to be retrieved. Multiple fields should be separated by commas.

        Example Input:
            fields=id,name,ima_formula,ima_symbol,ima_year,discovery_year,ima_status,ima_notes,type_specimen_store,mindat_longid,mindat_guid,type_localities,description_short,mindat_formula,mindat_formula_note,~all,*
        Returns:
            self: The MineralsIMARetriever object.
        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.fields("id,name,ima_formula")
            >>> mir.saveto()
        '''

        self._params.update({
            'fields': FIELDS
        })

        return self
    
    def id__in(self, ID_IN_LIST):
        '''
        Set the IDs for the query.

        Args:
            ID_IN_LIST (str): The IDs to filter the query, separated by commas.

        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.id__in("123,456,789")
            >>> mir.saveto()
        '''

        ids = str(ID_IN_LIST)

        self._params.update({
            'id__in': ids
        })

        return self

    def ima(self, IS_IMA):
        '''
            This filter is probably not working as intended. Just ignore it for now.
            Include IMA-approved names only (1) / to be determined(0)

            Args:
                IS_IMA (int): The IMA status to filter the query. 1 for IMA-approved names only, 0 is not clear.

            Returns:
                self: The MineralsIMARetriever object.

            Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.ima(1)
            >>> mir.saveto()
        '''

        if int(IS_IMA) not in [0, 1]:
            raise ValueError(f"Invalid IS_IMA: {IS_IMA}\nIS_IMA must be either 0 or 1.")

        ima = int(IS_IMA)
        self._params.update({
            'ima': ima
        })

        return self
    
    def omit(self, OMIT_FIELDS):
        '''
        Set the fields to omit from the query.

        Args:
            OMIT_FIELDS (str): The fields to omit, separated by commas. 
            Please check the API documentation for the list of available fields.
            https://api.mindat.org/schema/redoc/#tag/minerals_ima/operation/minerals_ima_list
        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.omit("id,name")
            >>> mir.saveto()
        '''

        omit_fields = OMIT_FIELDS
        self._params.update({
            'omit': omit_fields
        })

        return self
    
    def page(self, PAGE):
        '''
        Sets the page number within the paginated result set.

        Args:
            PAGE (int): The page number.

        Returns:
            self: The MineralsIMARetriever object.
        
        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.page(2)
            >>> mir.saveto()
        '''
        self._params.update({
            'page': PAGE
        })

        return self

    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The MineralsIMARetriever object.
            
        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.page_size(50)
            >>> mir.saveto()
        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def q(self, SEARCHING_KEYWORDS):
        '''
        Sets the keywords to search for.

        Args:
            SEARCHING_KEYWORDS (str): The keywords to search for.

        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.q("quartz")
            >>> mir.saveto()
        '''
        self._params.update({
            'q': SEARCHING_KEYWORDS
        })

        return self
    
    def updated_at(self, DATE_STR):
        '''	
            Sets the last updated datetime for the geomaterial query.

            Args:
                DATE_STR (str): The last updated datetime in the format %Y-%m-%d %H:%M:%S.

            Returns:
                self: The MineralsIMARetriever object.

            Raises:
                ValueError: If the provided DATE_STR is not a valid datetime string.

            Example:
                >>> retriever = GeomaterialRetriever()
                >>> retriever.updated_at('2022-01-01 12:00:00')
                >>> retriever.save()
        '''
        try:
            datetime.strptime(DATE_STR, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid datetime format. Please provide the datetime in the format %Y-%m-%d %H:%M:%S.")

        self._params.update({
            'updated_at': DATE_STR
        })

        return self
    
    def saveto(self, OUTDIR='', FILE_NAME = ''):
        '''
            Executes the query to retrieve the geomaterials with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved geomaterials will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> mir = MineralsIMARetriever()
                >>> mir.saveto("/path/to/directory")
        '''

        params = self._params
        end_point = self.end_point
        outdir = OUTDIR
        file_name = FILE_NAME

        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name)

        # reset the query parameters in case the user wants to make another query
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of geomaterials and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name
                
            Returns:
                None

            Example:
                >>> mir = MineralsIMARetriever()
                >>> mir.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve the list of mineral data and returns the json object.

        Returns:
            list of dictionaries.

        Example:
                >>> mir = MineralsIMARetriever()
                >>> quartsIMA = mir.q('quartz').get_dict()

        '''
       
        params = self._params
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
        
        self._init_params()
        return results
        
        
class MineralsIdRetriever:
    """
    This module provides the MineralsIdRetriever class for returning Minerals by id
    For more information visit: https://api.mindat.org/schema/redoc/#tag/minerals_ima/operation/minerals_ima_retrieve

    Usage:
        >>> midr = MineralsIdRetriever()
        >>> midr.id(5)

    Attributes:
        id (int): An int to store id parameter.
    """
    
    def __init__(self):
        self.end_point = 'minerals_ima'
        self.sub_endpoint = ''
        
        self._params = {}
        self._init_params()

    def _init_params(self):
        self.end_point = 'minerals_ima'
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
            self: The MineralsIdRetriever object.

        Example:
            >>> Midr = MineralsIdRetriever()
            >>> Midr.page_size(50)
            >>> Midr.save()

        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self

    def id(self, ID):
        '''
        Returns locality with matching id

        Args:
            id (INT): The locality id.

        Returns:
            self: The MineralsIdRetriever() object.

        Example:
            >>> midr = MineralsIdRetriever()
            >>> midr.id(2)
            >>> midr.save()
        '''
        
        try:
            ID = int(ID)
        except ValueError:
            raise ValueError("Invalid input. ID must be a valid integer.")
        
        id = str(ID)
        
        self.sub_endpoint = id
        
        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the Minerals with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved Minerals will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> midr = MineralsIdRetriever()
                >>> midr.id(3).saveto("/path/to/directory", "Mineral_ima_id")
        '''

        params = self._params
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        outdir = OUTDIR
        file_name = FILE_NAME

        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name)

        # reset the query parameters in case the user wants to make another query
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of minerals and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name
            
            Returns:
                None

            Example:
                >>> midr = MineralsIdRetriever()
                >>> midr.id(3).save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve mineral IMA status with a corresponding id and returns a dictionary.

        Returns:
            List of Dictionaries.

        Example:
                >>> midr = MineralsIdRetriever()
                >>> ima9 = midr.id(9).get_dict()

        '''
       
        params = self._params
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
        
        self._init_params()
        return results


if __name__ == '__main__':
    mir = MineralsIMARetriever()
    mir.ima('1').saveto()
