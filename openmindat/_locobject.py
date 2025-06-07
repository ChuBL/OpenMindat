from . import mindat_api


class LocobjectRetriever:
    """
    A class to facilitate the retrieval of loc object data from the Mindat API using an id
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locobject

    Methods:
        id(INT): returns the loc object with the matching id.
        saveto(OUTDIR, FILENAME): Executes the search query and saves the data to a specified directory.
        save(FILENAME): Executes the search query and saves the data to the current directory.

    Usage:
        >>> lor = LocobjectRetriever()
        >>> lor.id(5).save()

    Press q to quit.
    """

    BASE_ENDPOINT = 'locobject'
    
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
    
    def id(self, ID):
        '''
        Returns a loc object with the matching ID

        Args:
            id (INT): The loc object id.

        Returns:
            self: The LocobjectRetriver object.

        Example:
            >>> lor = LocobjectRetriever()
            >>> lor.id(2)
            >>> lor.save()
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
            >>> Lor = LocobjectRetriever()
            >>> Lor.verbose(0).saveto("/path/to/directory")

        '''
        if isinstance(FLAG, int):
            flag = FLAG
        else:
            raise ValueError(f"Possible Invalid ENTRYTYPE: {FLAG}\nPlease retry.")
        
        self.verbose_flag = flag
        
        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the loc object with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved loc object will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> lor = LocobjectRetriever()
                >>> lor.saveto("/path/to/directory")
        '''

        params = self._params
        outdir = OUTDIR
        end_point =  '/'.join([self.end_point, self.sub_endpoint])
        file_name = FILE_NAME
        verbose = self.verbose_flag
        
        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name, verbose)

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of loc object data and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> lor = LocobjectRetriever()
                >>> lor.id(3).save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve locobject with a corresponding id and returns a dictionary.

        Returns:
            List of Dictionaries.

        Example:
            >>> lor = LocobjectRetriever()
            >>> lor.id(2)
            >>> loco2 = lor.get_dict()

        '''
       
        params = self._params
        verbose = self.verbose_flag
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point, verbose)
        
        self._init_params()
        return results
    
    def available_methods(self):
        '''
        Prints the available methods of the class.

        Example:
            >>> lor = LocobjectRetriever()
            >>> lor.available_methods()
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
    lor = LocobjectRetriever()
    lor.id(2).save()
