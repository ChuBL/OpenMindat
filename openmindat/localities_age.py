from . import mindat_api


class LocalitiesAgeRetriever:
    """
    A class to facilitate the retrieval of locality data from the Mindat API filtered by page.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_age

    Methods:
        page(INT): returns a page of localities.
        saveto(OUTDIR, FILENAME): Executes the search query and saves the data to a specified directory.
        save(FILENAME): Executes the search query and saves the data to the current directory.

    Usage:
        >>> lar = LocalitiesAgeRetriever()
        >>> lar.page(2).save()

    Press q to quit.
    """
    
    def __init__(self):
        self.end_point = 'locality_age' 
        
        self._params = {}
        self._init_params()
    
    def _init_params(self):
        self.end_point = 'locality_age' 
        self._params.clear()
        self._params = {'format': 'json'}
        self.page_size(1500)
        
    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The LocalitiesAgeRetriever object.
            
        Example:
            >>> lar = LocalitiesAgeRetriever()
            >>> lar.page_size(50)
            >>> lar.saveto()
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
            self: The LocalitiesAgeRetriver object.

        Example:
            >>> lar = LocalitiesAgeRetriever()
            >>> lar.page(2)
            >>> lar.save()
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
                >>> lar = LocalityAgeRetriever()
                >>> lar.saveto("/path/to/directory")
        '''

        params = self._params
        outdir = OUTDIR
        end_point = self.end_point
        file_name = FILE_NAME
        
        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name)
            

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
                >>> lar = LocalitiesAgeRetriever()
                >>> lar.page(2).save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve the locality age data as a list of dictionaries.

        Returns:
            list of dictionaries.

        Example:
                >>> lar = LocalitiesAgeRetriever()
                >>> secondAgePage = lar.page(2).get_dict()

        '''
       
        params = self._params
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
            
        self._init_params()
        return results
        
        
class LocalitiesAgeIdRetriever:
    """
    A class to facilitate the retrieval of locality data from the Mindat API filtered by id.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_age/operation/locality_age_retrieve

    Methods:
        id(INT): returns the country with the matching id.
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

    Usage:
        >>> lair = LocalitiesAgeIdRetriever()
        >>> lair.id(5).save()

    Press q to quit.
    """
    
    def __init__(self):
        self.end_point = 'locality_age'
        self.sub_endpoint = ''
        
        self._params = {}
        self._init_params()
    
    def _init_params(self):
        self.end_point = 'locality_age'
        self.sub_endpoint = ''
        self._params.clear()
        self.page_size(1500)
        self._params = {'format': 'json'}
        
    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The LocalitiesAgeIdRetriever object.

        Example:
            >>> laidr = LocalitiesAgeIdRetriever()
            >>> laidr.page_size(2)
            >>> laidr.save()

        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def id(self, ID):
        '''
        Returns a country with the matching ID

        Args:
            id (INT): The country id.

        Returns:
            self: The LocalitiesAgeIdRetriver object.

        Example:
            >>> lair = LocalitiesAgeIdRetriever()
            >>> lair.id(2)
            >>> lair.save()
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
                >>> lair = LocalitiesAgeIdRetriever()
                >>> lair.id(4).saveto("/path/to/directory")
        '''

        params = self._params
        outdir = OUTDIR
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        file_name = FILE_NAME
        
        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name)

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
                >>> lair = localitiesAgeIdRetriever()
                >>> lair.id(2).save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve locality with a corresponding id and returns a dictionary.

        Returns:
            List of Dictionaries.

        Example:
                >>> lair = localitiesAgeIdRetriever()
                >>> localityAge2 = lair.id(2).get_dict()

        '''
       
        params = self._params
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
        
        self._init_params()
        return results

if __name__ == '__main__':
    lair = LocalitiesAgeIdRetriever()
    lair.id(2).save()
