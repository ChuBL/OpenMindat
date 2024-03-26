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
    
    def __init__(self):
       self.end_point = 'locobject' 
       self.sub_endpoint = ''
        
       self._params = {}
       self._init_params()
    
    def _init_params(self):
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
        
        print("Retrieving loc object. This may take a while... ")

        params = self._params
        outdir = OUTDIR
        end_point =  '/'.join([self.end_point, self.sub_endpoint])
        file_name = FILE_NAME
        
        ma = mindat_api.MindatApi()
        ma.get_mindat_item(params, end_point, outdir, file_name)

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
        
    def get_list(self):
        '''
        Executes the query to retrieve locobject with a corresponding id and returns a dictionary.

        Returns:
            dictionary.

        Example:
            >>> lor = LocobjectRetriever()
            >>> lor.id(2)
            >>> loco2 = lor.get_list()

        '''
        
        print("Retrieving locObject. This may take a while... ")
       
        params = self._params
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        
        #clears params for next get statement     
        self._init_params()
        
        ma = mindat_api.MindatApi()
        return ma.get_mindat_dict(params, end_point)

if __name__ == '__main__':
    lor = LocobjectRetriever()
    lor.id(2).save()
