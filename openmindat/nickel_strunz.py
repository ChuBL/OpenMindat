from . import mindat_api

#todo: Check back in when retrieve and id functions are implemented

class StrunzRetriever:
    """
    A class to facilitate the retrieval of nickel strunz 10 data from the Mindat API filtering with type of classes or subclasses.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/nickel-strunz-10
    
    This class allows for method chaining but if more than one method is used it will only return data for the last method used.

    Methods:
        retrieve: N/A
        id: N/A
        families: returns family information
        classes: returns classes information
        subClasses: returns subClasses information

    Usage:
        >>> sr = StrunzRetriever()
        >>> sr.classes().save()

    Press q to quit.
    """
    
    def __init__(self):
        self.end_point = 'nickel-strunz-10'
        self.sub_endpoint = '' 
        
        self._params = {}
        self._init_params()
    
    def _init_params(self):
        self.end_point = 'nickel-strunz-10'
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
            self: The StrunzRetriever object.

        Example:
            >>> sr = StrunzRetriever()
            >>> sr.page_size(1500)
            >>> sr.save()

        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
        
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
        
        self.sub_endpoint = ''
        
        return self        
        
    def id(self, ID):
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
        
        try:
            ID = int(ID)
        except ValueError:
            raise ValueError("Invalid input. ID must be a valid integer.")
        
        id = str(ID)
        
        self.sub_endpoint = id
        
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
        
        self.sub_endpoint = 'classes'
        
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

        self.sub_endpoint = 'subclasses'
        
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

        self.sub_endpoint = 'families'
        
        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the nickel strunz data with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved nickel strunz data will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> sr = strunzRetriever()
                >>> sr.families.saveto("/path/to/directory")
        '''

        params = self._params
        outdir = OUTDIR
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        file_name = FILE_NAME
        
        ma = mindat_api.MindatApi()
        
        if 'classes' in self.sub_endpoint:
            ma.download_mindat_json(params, end_point, outdir, file_name)
        else:
            ma.download_mindat_json(params, end_point, outdir, file_name)

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of nickel strunz data and saves the results to the current directory.
            
            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> sr = StrunzRetriever()
                >>> sr.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve the nickel_strunz data as a list of dictionaries.

        Returns:
            list of dictionaries.

        Example:
                >>> sr = StrunzRetriever()
                >>> nickelStrunzClasses = sr.classes().get_dict()
        '''
       
        params = self._params
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
            
        self._init_params()
        return results


if __name__ == '__main__':
    sr = StrunzRetriever()
    sr.classes().save()
