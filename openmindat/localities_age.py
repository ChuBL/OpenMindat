from . import mindat_api


class LocalitiesAgeRetriever:
    """
    A class to facilitate the retrieval of lacality data from the Mindat API filtered by page.

    Methods:
        page(INT): returns a page of localities.
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

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
        self._params.clear()
        self._params = {'format': 'json'}
    
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
        
        print("Retrieving localities. This may take a while... ")

        params = self._params
        outdir = OUTDIR
        end_point = self.end_point
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
                >>> lar = LocalitiesAgeRetriever()
                >>> lar.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
        
class LocalitiesAgeIdRetriever:
    """
    A class to facilitate the retrieval of lacality data from the Mindat API filtered by id.

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
        
       self._params = {}
       self._init_params()
    
    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}
    
    def id(self, ID :int):
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
        
        id = str(ID)
        
        self.end_point = (self.end_point + '/' + id)
        
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
                >>> lair.saveto("/path/to/directory")
        '''
        
        print("Retrieving localities. This may take a while... ")

        params = self._params
        outdir = OUTDIR
        end_point = self.end_point
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
                >>> lair = localitiesAgeIdRetriever()
                >>> lair.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)

if __name__ == '__main__':
    lair = LocalitiesAgeIdRetriever()
    lair.id(2).save()
