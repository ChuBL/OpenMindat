from . import mindat_api


class LocalitiesTypeRetriever:
    """
    A class to facilitate the retrieval of locolity data from the Mindat API filtered by page.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_type

    Methods:
        page(INT): returns a page of localities.
        saveto(OUTDIR, FILENAME): Executes the search query and saves the data to a specified directory.
        save(FILENAME): Executes the search query and saves the data to the current directory.

    Usage:
        >>> ltr = LocalitiesTypeRetriever()
        >>> ltr.page(2).save()

    Press q to quit.
    """

    BASE_ENDPOINT = 'locality-type'   

    def __init__(self):
        self.end_point = self.BASE_ENDPOINT
        self.verbose_flag = 2
        
        self._params = {}
        self._init_params()
    
    def _init_params(self):
        self.end_point = self.BASE_ENDPOINT
        self.verbose_flag = 2
        self._params.clear()
        self._params = {'format': 'json'}
        self.page_size(1500)
        
    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The LocalitiesTypeRetriever object.
            
        Example:
            >>> ltr = LocalitiesTypeRetriever()
            >>> ltr.page_size(50)
            >>> ltr.saveto()
        '''
        self._params.update({
            'page-size': PAGE_SIZE
        })

        return self
    
    def page(self, PAGE):
        '''
        Returns a page of locality data.

        Args:
            page (INT): The page number.

        Returns:
            self: The LocalitiesTypeRetriver object.

        Example:
            >>> ltr = LocalitiesTypeRetriever()
            >>> ltr.page(2)
            >>> ltr.save()
        '''
        
        page = PAGE
    
        self._params.update({
            "page": page
        })
        
        return self
    
    def verbose(self, FLAG):
        '''
        Determinse the verbose mode of the query.

        Args:
            FLAG (int): Determines the verbose mode: 0 = silent, 1 = save notifications, 2(default) = progress bar

        Returns:
            None

        Example:
            >>> Lar = LocalitiesAgeRetriever()
            >>> Lar.verbose(0).saveto("/path/to/directory")

        '''
        if isinstance(FLAG, int):
            flag = FLAG
        else:
            raise ValueError(f"Possible Invalid ENTRYTYPE: {FLAG}\nPlease retry.")
        
        self.verbose_flag = flag
        
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
                >>> ltr = LocalityTypeRetriever()
                >>> ltr.page(19).saveto("/path/to/directory")
        '''

        params = self._params
        outdir = OUTDIR
        end_point = self.end_point
        file_name = FILE_NAME
        verbose = self.verbose_flag
        
        ma = mindat_api.MindatApi()
        
        if "page" in params:
            ma.download_mindat_json(params, end_point, outdir, file_name, verbose)
        else:
            ma.download_mindat_json(params, end_point, outdir, file_name, verbose)
            

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
                >>> ltr = LocalitiesTypeRetriever()
                >>> ltr.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve the locality type data as a list of dictionaries.

        Returns:
            list of dictionaries.

        Example:
                >>> ltr = LocalitiesTypeRetriever()
                >>> secondTypePage = ltr.page(2).get_dict()
        '''
       
        params = self._params
        verbose = self.verbose_flag
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point, verbose)
            
        self._init_params()
        return results
    
    def available_methods(self):
        '''
        Prints the available methods of the class.

        Example:
            >>> ltr = LocalitiesTypeRetriever()
            >>> ltr.available_methods()
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
        
        
class LocalitiesTypeIdRetriever:
    """
    A class to facilitate the retrieval of locality data from the Mindat API filtered by id.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_type/operation/locality_type_retrieve

    Methods:
        id(INT): returns the country with the matching id.
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

    Usage:
        >>> ltir = LocalitiesTypeIdRetriever()
        >>> ltir.id(5).save()

    Press q to quit.
    """

    BASE_ENDPOINT = 'locality-type'   
    
    def __init__(self):
        self.end_point = self.BASE_ENDPOINT
        self.verbose_flag = 2
        self.sub_endpoint = ''
        
        self._params = {}
        self._init_params()
    
    def _init_params(self):
        self.end_point = self.BASE_ENDPOINT
        self.verbose_flag = 2
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
            self: The LocalitiesTypeIdRetriever object.
            
        Example:
            >>> ltidr = LocalitiesTypeIdRetriever()
            >>> ltidr.id(50)
            >>> ltidr.saveto()
        '''
        self._params.update({
            'page-size': PAGE_SIZE
        })

        return self
    
    def id(self, ID):
        '''
        Returns a country with the matching ID

        Args:
            id (INT): The country id.

        Returns:
            self: The LocalitiesTypeIdRetriver object.

        Example:
            >>> ltir = LocalitiesTypeIdRetriever()
            >>> ltir.id(2)
            >>> ltir.save()
        '''
        
        try:
            ID = int(ID)
        except ValueError:
            raise ValueError("Invalid input. ID must be a valid integer.")
        
        id = str(ID)
        
        self.sub_endpoint = id
        
        return self
    
    def verbose(self, FLAG):
        '''
        Determinse the verbose mode of the query.

        Args:
            FLAG (int): Determines the verbose mode: 0 = silent, 1 = save notifications, 2(default) = progress bar

        Returns:
            None

        Example:
            >>> lsidr = LocalitiesAgeIdRetriever()
            >>> lsidr.id(3).verbose(0).saveto("/path/to/directory")

        '''
        if isinstance(FLAG, int):
            flag = FLAG
        else:
            raise ValueError(f"Possible Invalid ENTRYTYPE: {FLAG}\nPlease retry.")
        
        self.verbose_flag = flag
        
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
                >>> ltir = LocalitiesTypeIdRetriever()
                >>> ltir.id(2).saveto("/path/to/directory")
        '''

        params = self._params
        outdir = OUTDIR
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        file_name = FILE_NAME
        verbose = self.verbose_flag
        
        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name, verbose)

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
                >>> ltir = localitiesTypeIdRetriever()
                >>> ltir.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve locality type with a corresponding id and returns a dictionary.

        Returns:
            List of Dictionaries.

        Example:
                >>> ltir = localitiesTypeIdRetriever()
                >>> localityType2 = ltir.id(2).get_dict()

        '''
       
        verbose = self.verbose_flag
        params = self._params
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point, verbose)
        
        self._init_params()
        return results
    
    def available_methods(self):
        '''
        Prints the available methods of the class.

        Example:
            >>> ltidr = LocalitiesTypeIdRetriever()
            >>> ltidr.available_methods()
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

if __name__ == '__main__':
    ltir = LocalitiesTypeIdRetriever()
    ltir.id(2).save()
