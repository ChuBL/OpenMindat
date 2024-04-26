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
        self.end_point = 'photocount' 
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
            'page_size': PAGE_SIZE
        })

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
        file_name = FILE_NAME
        
        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name)

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
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
        
        self._init_params()
        return results

if __name__ == '__main__':
    pcr = PhotoCountRetriever()
    pcr.save()
