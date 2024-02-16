from . import mindat_api

class GeomaterialSearchRetriever:
    """
    A class to facilitate the retrieval of geomaterial data from the Mindat API using search keywords. It enables users to construct queries based on specific keywords and offers functionality to save the retrieved data.

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
            >>> gr = GeomaterialRetriever()
            >>> gr.geomaterials_search("quartz, green, hexagonal")
            >>> gr.save()
        '''
        keywords = KEYWORDS
        self._params.update({'q': keywords})
        return self
    
    def saveto(self, OUTDIR = ''):
        '''
            Executes the query to retrieve the geomaterials with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved geomaterials will be saved. If not provided, the current directory will be used.

            Returns:
                None
        '''

        print("Retrieving geomaterials. This may take a while... ")
        
        params = self._params
        end_point = 'geomaterials_search'
        outdir = OUTDIR

        ma = mindat_api.MindatApi()
        ma.get_mindat_search(params, end_point, outdir)

        # reset the query parameters in case the user wants to make another query
        self._init_params()

    def save(self):
        '''
            Executes the query to retrieve the list of geomaterials and saves the results to the current directory.

            Returns:
                None
        '''
        self.saveto()


if __name__ == '__main__':
    gsr = GeomaterialSearchRetriever()
    gsr.geomaterials_search("quartz, green, hexagonal").save()