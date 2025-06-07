from . import mindat_api

class PhotoCountRetriever:
    """
    A class to facilitate the retrieval of photo count data from the Mindat API.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/photocount
    
    Methods:
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

    Usage:
        >>> pcr = PhotoCountRetriever()
        >>> pcr.save()

    Press q to quit.
    """
    
    def __init__(self):
        self.end_point = 'photocount'
        self.verbose_flag = 2 
        
        self._params = {}
        self._init_params()
    
    def _init_params(self):
        self.end_point = 'photocount' 
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
            self: The PhotoCountRetriever object.

        Example:
            >>> pcr = PhotoCountRetriever()
            >>> pcr.page_size(1500)
            >>> pcr.save()

        '''
        self._params.update({
            'page-size': PAGE_SIZE
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
            >>> pcr = PhotoCountRetriever()
            >>> pcr.verbose(0).saveto("/path/to/directory")

        '''
        if isinstance(FLAG, int):
            flag = FLAG
        else:
            raise ValueError(f"Possible Invalid ENTRYTYPE: {FLAG}\nPlease retry.")
        
        self.verbose_flag = flag
        
        return self
    
    #when fixed check if this needs get item or get list
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the photo count with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved localities will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> pcr = PhotoCountRetriever()
                >>> pcr.saveto("/path/to/directory")
        '''

        params = self._params
        outdir = OUTDIR
        end_point = self.end_point
        verbose = self.verbose_flag
        file_name = FILE_NAME
        
        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name, verbose)

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of photo count data and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> pcr = PhotoCountRetriever()
                >>> pcr.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve photo counts and returns a dictionary.

        Returns:
            List of Dictionaries.

        Example:
                >>> pcr = PhotoCountRetriever()
                >>> photoCount = pcr.get_dict()

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
            >>> pcr = PhotoCountRetriever()
            >>> pcr.available_methods()
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
    pcr = PhotoCountRetriever()
    pcr.save()
