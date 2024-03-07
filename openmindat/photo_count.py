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
        
       self._params = {}
       self._init_params()
    
    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}
    
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
        
        print("Retrieving photo count. This may take a while... ")

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

if __name__ == '__main__':
    pcr = PhotoCountRetriever()
    pcr.save()
