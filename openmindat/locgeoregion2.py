from . import mindat_api


class GeoRegionRetriever:
    """
    A class to facilitate the retrieval of locality geoRegion data from the Mindat API filtered by page.
    for more information visit: https://api.mindat.org/schema/redoc/#tag/locgeoregion2

    Methods:
        page(INT): returns a page of localities.
        saveto(OUTDIR, FILENAME): Executes the search query and saves the data to a specified directory.
        save(FILENAME): Executes the search query and saves the data to the current directory.

    Usage:
        >>> grr = GeoRegionRetriever()
        >>> grr.page(2).save()

    Press q to quit.
    """
    
    def __init__(self):
        self.end_point = 'locgeoregion2' 
        
        self._params = {}
        self._init_params()
    
    def _init_params(self):
        self.end_point = 'locgeoregion2' 
        self._params.clear()
        self._params = {'format': 'json'}
        self.page_size(1500)
        
    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The GeoRegionRetriever object.
            
        Example:
            >>> grr = GeoRegionRetriever()
            >>> grr.page_size(50)
            >>> grr.saveto()
        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def page(self, PAGE):
        '''
        Returns a page of locality data.

        Args:
            page (INT): The page number.

        Returns:
            self: The GeoRegionRetriver object.

        Example:
            >>> grr = GeoRegionRetriever()
            >>> grr.page(2)
            >>> grr.save()
        '''
        
        page = PAGE
    
        self._params.update({
            "page": page
        })
        
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
                >>> grr = GeoRegionRetriever()
                >>> grr.saveto("/path/to/directory")
        '''

        params = self._params
        outdir = OUTDIR
        end_point = self.end_point
        file_name = FILE_NAME
        
        ma = mindat_api.MindatApi()
        
        if "page" in params:
            ma.download_mindat_json(params, end_point, outdir, file_name)
        else:
            ma.download_mindat_json(params, end_point, outdir, file_name)
            

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
                >>> grr = GeoRegionRetriever()
                >>> grr.page(3).save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve the geoRegion data as a list of dictionaries.

        Returns:
            list of dictionaries.

        Example:
                >>> grr = GeoRegionRetriever()
                >>> georegion3 = grr.page(3).get_dict()
        '''
       
        params = self._params
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
            
        self._init_params()
        return results
            
            
if __name__ == '__main__':
    grr = GeoRegionRetriever()
    grr.page(1).save()