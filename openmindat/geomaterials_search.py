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
    def __init__(self):
       self._params = {}
       self.end_point = 'geomaterials_search'
    
    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}

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
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the geomaterials with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved geomaterials will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None
        '''
        print("Retrieving geomaterials. This may take a while... ")
        
        params = self._params
        end_point = self.end_point
        outdir = OUTDIR
        file_name = FILE_NAME

        ma = mindat_api.MindatApi()
        ma.get_mindat_search(params, end_point, outdir, file_name)

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
        
    def get_list(self):
        '''
        Executes the query to retrieve the geomaterial search data as a dictionary.

        Returns:
            List of dictionaries.

        Example:
            >>> gsr = geomaterialSeachRetriever()
            >>> greenQuarts = gsr.geomaterial_search("quartz, green").get_list()

        '''
        
        print("Retrieving geomaterial search. This may take a while... ")
       
        params = self._params
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()
        results = [ma.get_mindat_dict(params, end_point)]
        
        self._init_params()
        return results


if __name__ == '__main__':
    gsr = GeomaterialSearchRetriever()
    gsr.geomaterials_search("quartz, green, hexagonal").save()