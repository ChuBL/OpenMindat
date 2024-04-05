from . import mindat_api


class LocalitiesStatusRetriever:
    """
    A class to facilitate the retrieval of locality data from the Mindat API filtered by page.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_status

    Methods:
        page(INT): returns a page of localities.
        saveto(OUTDIR, FILENAME): Executes the search query and saves the data to a specified directory.
        save(FILENAME): Executes the search query and saves the data to the current directory.

    Usage:
        >>> lsr = LocalitiesStatusRetriever()
        >>> lsr.page(2).save()

    Press q to quit.
    """
    
    def __init__(self):
       self.end_point = 'locality_status' 
        
       self._params = {}
       self._init_params()
    
    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}
        self.page_size(1500)
        
    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The LocalitiesStatusRetriever object.
            
        Example:
            >>> lsr = LocalitiesStatusRetriever()
            >>> lsr.page_size(50)
            >>> lsr.saveto()
        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def page(self, PAGE):
        '''
        Returns a page of locality data.

        Args:
            page (INT): The page number.

        Returns:
            self: The LocalitiesStatusRetriver object.

        Example:
            >>> lsr = LocalitiesStatusRetriever()
            >>> lsr.page(2)
            >>> lsr.save()
        '''
        
        page = PAGE
    
        self._params.update({
            "page": page
        })
        
        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the localities with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved localities will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> lsr = LocalityStatusRetriever()
                >>> lsr.saveto("/path/to/directory")
        '''
        
        print("Retrieving localities. This may take a while... ")

        params = self._params
        outdir = OUTDIR
        end_point = self.end_point
        file_name = FILE_NAME
        
        ma = mindat_api.MindatApi()
        
        if "page" in params:
            ma.get_mindat_item(params, end_point, outdir, file_name)
        else:
            ma.get_mindat_list(params, end_point, outdir, file_name)
            

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of locality data and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> lsr = LocalitiesStatusRetriever()
                >>> lsr.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_object(self):
        '''
        Executes the query to retrieve the locality status data as a list of dictionaries.

        Returns:
            list of dictionaries, or a dictionary if "page" parameter is included.

        Example:
                >>> lsr = LocalitiesStatusRetriever()
                >>> secondAgePage = lsr.page(2).get_object()

        '''
        
        print("Retrieving localities search. This may take a while... ")
       
        params = self._params
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()
        #clears params for next get statement     
        self._init_params()
        
        if "page" in params:
            return ma.get_mindat_dict(params, end_point)
        else:
            return ma.get_mindat_list_object(params, end_point)
        
        
class LocalitiesStatusIdRetriever:
    """
    A class to facilitate the retrieval of locality data from the Mindat API filtered by id.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_status/operation/locality_status_retrieve

    Methods:
        id(INT): returns the country with the matching id.
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

    Usage:
        >>> lsir = LocalitiesStatusIdRetriever()
        >>> lsir.id(5).save()

    Press q to quit.
    """
    
    def __init__(self):
       self.end_point = 'locality_status' 
       self.sub_endpoint = ''
        
       self._params = {}
       self._init_params()
    
    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}
    
    def id(self, ID):
        '''
        Returns a country with the matching ID

        Args:
            id (INT): The country id.

        Returns:
            self: The LocalitiesStatusIdRetriver object.

        Example:
            >>> lsir = LocalitiesStatusIdRetriever()
            >>> lsir.id(2)
            >>> lsir.save()
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
            Executes the query to retrieve the localities with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved localities will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> lsir = LocalitiesStatusIdRetriever()
                >>> lsir.saveto("/path/to/directory")
        '''
        
        print("Retrieving localities. This may take a while... ")

        params = self._params
        outdir = OUTDIR
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        file_name = FILE_NAME
        
        ma = mindat_api.MindatApi()
        ma.get_mindat_item(params, end_point, outdir, file_name)

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of locality data and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> lsir = localitiesStatusIdRetriever()
                >>> lsir.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve locality status with a corresponding id and returns a dictionary.

        Returns:
            dictionary.

        Example:
                >>> lsir = localitiesStatusIdRetriever()
                >>> localitystatus2 = lsir.id(2).get_dict()

        '''
        
        print("Retrieving localities. This may take a while... ")
       
        params = self._params
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        
        #clears params for next get statement     
        self._init_params()
        
        ma = mindat_api.MindatApi()
        return ma.get_mindat_dict(params, end_point)

if __name__ == '__main__':
    lsir = LocalitiesStatusIdRetriever()
    lsir.id(2).save()
