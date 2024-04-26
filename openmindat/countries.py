from . import mindat_api


class CountriesListRetriever:
    """
    A class to facilitate the retrieval of country data from the Mindat API using by page.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/countries/operation/countries_list

    Methods:
        page(INT): returns a page of countries.
        saveto(OUTDIR, FILENAME): Executes the search query and saves the data to a specified directory.
        save(FILENAME): Executes the search query and saves the data to the current directory.

    Usage:
        >>> cr = CountriesListRetriever()
        >>> cr.page(2).save()

    Press q to quit.
    """
    
    def __init__(self):
        self.end_point = 'countries' 
        
        self._params = {}
        self._init_params()
    
    def _init_params(self):
        self.end_point = 'countries' 
        self._params.clear()
        self._params = {'format': 'json'}
        self.page_size(1500)
    
    def page(self, PAGE):
        '''
        Returns a page of country data.

        Args:
            page (INT): The page number.

        Returns:
            self: The CountriesRetriver object.

        Example:
            >>> cr = CountriesListRetriever()
            >>> cr.page(2)
            >>> cr.save()
        '''
        
        page = PAGE
    
        self._params.update({
            "page": page
        })
        
        return self
    
    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The CountriesListRetriever object.

        Example:
            >>> cr = CountriesListRetriever()
            >>> cr.page_size(2)
            >>> cr.save()

        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the countries with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved countries will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> cr = CountriesListRetriever()
                >>> cr.page(2).saveto("/path/to/directory")
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
            Executes the query to retrieve the country data and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> cr = CountriesListRetriever()
                >>> cr.page(2).save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_list(self):
        '''
        Executes the query to retrieve the country data as a dictionary.

        Returns:
            list of dictionaries.

        Example:
            >>> cr = CountriesListRetriever()
            >>> france = cr.page(2).get_list()

        '''
       
        params = self._params
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()        
        #clears params for next get statement     

        if "page" in params:
            results = [ma.get_mindat_json(params, end_point)]
        else:
            results = ma.get_mindat_json(params, end_point)
        
        
        self._init_params()
        return results
            
            
        

class CountriesIdRetriever:
    """
    A class to facilitate the retrieval of country data from the Mindat API using an id.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/countries/operation/countries_retrieve

    Methods:
        id(INT): returns the country with the matching id.
        saveto(OUTDIR, FILENAME): Executes the search query and saves the data to a specified directory.
        save(FILENAME): Executes the search query and saves the data to the current directory.

    Usage:
        >>> cidr = CountriesIdRetriever()
        >>> cidr.id(5).save()

    Press q to quit.
    """
    
    def __init__(self):
        self.end_point = 'countries' 
        
        self._params = {}
        self._init_params()
    
    def _init_params(self):
        self.end_point = 'countries' 
        self._params.clear()
        self._params = {'format': 'json'}
        self.page_size(1500)
        
    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The CountriesIdRetriever object.

        Example:
            >>> cidr = CountriesListIdRetriever()
            >>> cidr.page_size(2)
            >>> cidr.save()

        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def id(self, ID):
        '''
        Returns a country with the matching ID

        Args:
            id (INT): The country id.

        Returns:
            self: The CountriesIdRetriver object.

        Example:
            >>> cidr = CountriesIdRetriever()
            >>> cidr.id(2)
            >>> cidr.save()
        '''
        
        try:
            ID = int(ID)
        except ValueError:
            raise ValueError("Invalid input. ID must be a valid integer.")
        
        id = str(ID)
        
        self.end_point = '/'.join([self.end_point, id])
        
        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the countries with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved countries will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> cidr = CountriesIdRetriever()
                >>> cidr.id(2).saveto("/path/to/directory")
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
            Executes the query to retrieve the list of country data and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> cidr = countriesIdRetriever()
                >>> cidr.id(2).save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_list(self):
        '''
        Executes the query to retrieve the country data as a dictionary.

        Returns:
            list of dictionaries.

        Example:
            >>> cidr = countriesIdRetriever()
            >>> france = cidr.id(2).get_liat()

        '''
       
        params = self._params
        end_point = self.end_point    
        
        ma = mindat_api.MindatApi()
        results = [ma.get_mindat_json(params, end_point)]
        
        self._init_params()
        return results

if __name__ == '__main__':
    cidr = CountriesIdRetriever()
    cidr.id(2).save()
