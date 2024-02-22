from . import mindat_api

#todo: Check back in when retrieve and id functions are implemented

class StrunzRetriever:
    """
    A class to facilitate the retrieval of nickel strunz 10 data from the Mindat API filtering with type of groups or subgroups.
    
    This class allows for method chaining but if more than one method is used it will only return data for the last method used.

    Methods:
        retrieve: N/A
        id: N/A
        families: returns family information
        classes: returns classes information
        subClasses: returns subClasses information

    Usage:
        >>> sr = StrunzRetriever()
        >>> sr.groups().save()

    Press q to quit.
    """
    
    def __init__(self):
       self.path = '' 
        
       self._params = {}
       self._init_params()
    
    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}
        
    def retrieve(self):
        '''
        Returns Nickel Strunz classification
        Not yet working

        Returns:
            self: The StrunzRetriver object.

        Example:
            >>> sr = StrunzRetriever()
            >>> sr.retrieve()
            >>> sr.save()
        '''
        
        self.path = ''
        
        return self        
        
    def id(self, ID :int):
        '''
        Returns Nickel Strunz classification with matching id
        Not yet working

        Args:
            id (INT): The nickel strunz id.

        Returns:
            self: The StrunzRetriver object.

        Example:
            >>> sr = StrunzRetriever()
            >>> sr.id(2)
            >>> sr.save()
        '''
        
        id = str(ID)
        
        self.path = '/' + id
        
        return self
    
    def classes(self):
        '''
        Returns nickel strunz 10th edition classifications.

        Returns:
            self: The StrunzRetriever object.

        Example:
            >>> sr = StrunzRetriever()
            >>> sr.classes()
            >>> sr.save()
        '''
        
        self.path = '/classes'
        
        return self
    
    def subclasses(self):
        '''
        Returns nickel strunz 10th edition subgroup classifications.

        Returns:
            self: The StrunzRetriever object.

        Example:
            >>> sr = StrunzRetriever()
            >>> sr.subclasses()
            >>> sr.save()
        '''

        self.path = '/subclasses'
        
        return self
    
    def families(self):
        '''
        Returns nickel strunz 10th edition family classifications.

        Returns:
            self: The StrunzRetriever object.

        Example:
            >>> sr = StrunzRetriever()
            >>> sr.families()
            >>> sr.save()
        '''

        self.path = '/families'
        
        return self
    
    def saveto(self, OUTDIR=''):
        '''
            Executes the query to retrieve the nickel strunz data with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved nickel strunz data will be saved. If not provided, the current directory will be used.

            Returns:
                None

            Example:
                >>> sr = strunzRetriever()
                >>> sr.saveto("/path/to/directory")
        '''
        
        print("Retrieving nickel strunz Data. This may take a while... ")

        params = self._params
        outdir = OUTDIR
        end_point = 'nickel-strunz-10' + self.path
        
        ma = mindat_api.MindatApi()
        
        if '/classes' in self.path:
            ma.get_mindat_item(params, end_point, outdir)
        else:
            ma.get_mindat_list(params, end_point, outdir)

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()
    
    def save(self):
        '''
            Executes the query to retrieve the list of nickel strunz data and saves the results to the current directory.

            Returns:
                None

            Example:
                >>> sr = StrunzRetriever()
                >>> sr.save()
        '''
        self.saveto()


if __name__ == '__main__':
    sr = StrunzRetriever()
    sr.groups().save()
