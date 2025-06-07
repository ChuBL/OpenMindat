from . import mindat_api

#todo: Check back in when retrieve and id functions are implemented

class DanaRetriever:
    """
    A class to facilitate the retrieval of dana-8 data from the Mindat API filtering with type of groups or subgroups.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/dana-8/operation/dana_8_retrieve
    
    This class allows for method chaining but if more than one method is used it will only return data for the last method used.

    Methods:
        retrieve: N/A
        id: N/A
        groups: returns group information
        subgroups: returns subgroup information

    Usage:
        >>> dr = DanaRetriever()
        >>> dr.groups().save()

    Press q to quit.
    """
    
    BASE_ENDPOINT = 'v1/dana-8'

    def __init__(self):
        self.sub_endpoint = ''
        self.end_point = self.BASE_ENDPOINT
        self.verbose_flag = 2
        
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
            self: The DanaRetriever object.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.page_size(1500)
            >>> dr.save()

        '''
        self._params.update({
            'page-size': PAGE_SIZE
        })

        return self
        
    def retrieve(self):
        '''
        Returns dana-8 classification
        Not yet working

        Returns:
            self: The DanaRetriver object.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.retrieve()
            >>> dr.save()
        '''
        
        self.sub_endpoint = ''
        
        return self        
        
    def id(self, ID):
        '''
        Returns dana-8 classification with matching id
        Not yet working

        Args:
            id (INT): The dana-8 id.

        Returns:
            self: The DanaRetriver object.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.id(2)
            >>> dr.save()
        '''
        try:
            ID = int(ID)
        except ValueError:
            raise ValueError("Invalid input. ID must be a valid integer.")
        
        id = str(ID)
        
        self.sub_endpoint = id
        
        return self
    
    def groups(self):
        '''
        Returns Dana 8th edition group classifications.

        Returns:
            self: The DanaRetriever object.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.groups()
            >>> dr.save()
        '''
        
        self.sub_endpoint = 'groups'
        
        return self
    
    def subgroups(self):
        '''
        Returns Dana 8th edition subgroup classifications.

        Returns:
            self: The DanaRetriever object.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.subgroups()
            >>> dr.save()
        '''

        self.sub_endpoint = 'subgroups'
        
        return self
    
    def verbose(self, FLAG):
        '''
        Determinse the verbose mode of the query.

        Args:
            FLAG (int): Determines the verbose mode: 0 = silent, 1 = save notifications, 2(default) = progress bar

        Returns:
            None

        Example:
            >>> dr = DanaRetriever()
            >>> dr.subgroups().verbose(0).saveto("/path/to/directory")
        '''
        
        if isinstance(FLAG, int):
            flag = FLAG
        else:
            raise ValueError(f"Possible Invalid ENTRYTYPE: {FLAG}\nPlease retry.")
        
        self.verbose_flag = flag
        
        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the dana-8 data with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved dana-8 data will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> dr = DanaRetriever()
                >>> dr.saveto("/path/to/directory")
        '''
        
        params = self._params
        outdir = OUTDIR
        file_name = FILE_NAME
        end_point = self.end_point
        verbose = self.verbose_flag
        
        if self.sub_endpoint != '':
            end_point = '/'.join([self.BASE_ENDPOINT, self.sub_endpoint])
        
        ma = mindat_api.MindatApi()

        ma.download_mindat_json(params, end_point, outdir, file_name, verbose)

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of dana-8 data and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> dr = DanaRetriever()
                >>> dr.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve the dana-8 data as a dictionary.

        Returns:
            list of dictionaries.

        Example:
            >>> dr = danaRetriever()
            >>> danaGroups = cr.group().get_dict()

        '''
       
        params = self._params       
        end_point = self.end_point 
        verbose = self.verbose_flag
        
        if self.sub_endpoint != '':
            end_point = '/'.join([self.BASE_ENDPOINT, self.sub_endpoint])
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point, verbose)
        
        self._init_params()
        return results
    
    def available_methods(self):
        '''
        Prints the available methods of the class.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.available_methods()
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
    dr = DanaRetriever()
    dr.groups().save()
