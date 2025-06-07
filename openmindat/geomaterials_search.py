from . import mindat_api

class GeomaterialSearchRetriever:
    """
    A class to facilitate the retrieval of geomaterial data from the Mindat API using search keywords. It enables users to construct queries based on specific keywords and offers functionality to save the retrieved data.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/geomaterials_search

    Methods:
        geomaterials_search(KEYWORDS): Updates the search query with specified keywords.
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

    Usage:
        >>> gsr = GeomaterialSearchRetriever()
        >>> gsr.geomaterials_search("quartz, green, hexagonal").save()

    Press q to quit.
    """

    BASE_ENDPOINT = 'v1/geomaterials-search'
    
    def __init__(self):
        self._params = {}
        self.end_point = self.BASE_ENDPOINT
        self.verbose_flag = 2
    
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
            self: The GeomaterialSearchRetriever object.

        Example:
            >>> gsr = GeomaterialSearchRetriever()
            >>> gsr.page_size(500)
            >>> gsr.save()

        '''
        self._params.update({
            'page-size': PAGE_SIZE
        })

        return self

    def geomaterials_search(self, KEYWORDS):
        '''
        Updates the query parameters to search for geomaterials based on specified keywords.

        Args:
            KEYWORDS (str): A string containing the keywords to search for. 

        Returns:
            self: The GeomaterialRetriever object, allowing for method chaining.

        Example:
            >>> gsr = GeomaterialSearchRetriever()
            >>> gsr.geomaterials_search("quartz, green, hexagonal")
            >>> gsr.save()
        '''
        keywords = KEYWORDS
        self._params.update({'q': keywords})
        return self
    
    def verbose(self, FLAG):
        '''
        Determinse the verbose mode of the query.

        Args:
            FLAG (int): Determines the verbose mode: 0 = silent, 1 = save notifications, 2(default) = progress bar

        Returns:
            None

        Example:
            >>> gsr = GeomaterialSearchRetriever()
            >>> gsr.geomaterials_Search("mica").verbose(0).saveto("/path/to/directory")

        '''
        if isinstance(FLAG, int):
            flag = FLAG
        else:
            raise ValueError(f"Possible Invalid ENTRYTYPE: {FLAG}\nPlease retry.")
        
        self.verbose_flag = flag
        
        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the geomaterials with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved geomaterials will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None
        '''
        
        params = self._params
        end_point = self.end_point
        outdir = OUTDIR
        file_name = FILE_NAME
        verbose = self.verbose_flag

        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name, verbose)

        # reset the query parameters in case the user wants to make another query
        self._init_params()

    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of geomaterials and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve the geomaterial search data as a dictionary.

        Returns:
            List of dictionaries.

        Example:
            >>> gsr = geomaterialSeachRetriever()
            >>> greenQuarts = gsr.geomaterial_search("quartz, green").get_dict()

        '''
       
        params = self._params
        end_point = self.end_point
        verbose = self.verbose_flag
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point, verbose)
        
        self._init_params()
        return results
    
    def available_methods(self):
        '''
        Prints the available methods of the class.

        Example:
            >>> gsr = GeomaterialSearchRetriever()
            >>> gsr.available_methods()
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
    gsr = GeomaterialSearchRetriever()
    gsr.geomaterials_search("quartz, green, hexagonal").save()