from . import mindat_api


class CountriesRetriever:
    """
    A class to facilitate the retrieval of country data from the Mindat API using an id or by page.

    Methods:
        id(INT): returns the country with the matching id.
        page(INT): returns a page of countries.
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

    Usage:
        >>> cr = CountriesRetriever()
        >>> cr.id(5).save()
        >>> cr.page(2).save()

    Press q to quit.
    """
    
    def __init__(self):
       self.end_point = 'countries' 
        
       self._params = {}
       self._init_params()
    
    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}
    
    def id(self, ID :int):
        '''
        Returns a country with the matching ID

        Args:
            id (INT): The country id.

        Returns:
            self: The CountriesRetriver object.

        Example:
            >>> cr = CountriesRetriever()
            >>> cr.id(2)
            >>> cr.save()
        '''
        
        id = str(ID)
        
        self.end_point = (self.end_point + '/' + id)
        
        return self
    
    def page(self, PAGE):
        '''
        Returns a page of country data.

        Args:
            page (INT): The page number.

        Returns:
            self: The CountriesRetriver object.

        Example:
            >>> cr = CountriesRetriever()
            >>> cr.page(2)
            >>> cr.save()
        '''
        
        page = PAGE
    
        self._params.update({
            "page": page
        })
        
        return self
    
    def saveto(self, OUTDIR=''):
        '''
            Executes the query to retrieve the countries with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved countries will be saved. If not provided, the current directory will be used.

            Returns:
                None

            Example:
                >>> cr = contriesRetriever()
                >>> cr.saveto("/path/to/directory")
        '''
        
        print("Retrieving Countries. This may take a while... ")

        params = self._params
        outdir = OUTDIR
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()
        ma.get_mindat_item(params, end_point, outdir)

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()
    
    def save(self):
        '''
            Executes the query to retrieve the list of country data and saves the results to the current directory.

            Returns:
                None

            Example:
                >>> cr = contriesRetriever()
                >>> cr.save()
        '''
        self.saveto()


if __name__ == '__main__':
    cr = CountriesRetriever()
    cr.iso("mx").save()
