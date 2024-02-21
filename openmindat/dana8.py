from . import mindat_api

#todo: Check back in when retrieve and id functions are implemented

class DanaRetriever:
    """
    A class to facilitate the retrieval of dana-8 data from the Mindat API filtering with type of groups or subgroups.
    
    This class allows for method chaining but if more than one method is used it will only return data for the last method used.

    Methods:
        retrieve: N/A
        id: N/A
        groups: returns group information
        subgroups: returns subgroup information

    Usage:
        >>> dr = Dana8_Retriever()
        >>> dr.groups().save()

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
        Returns dana-8 classification
        Not yet working

        Returns:
            self: The DanaRetriver object.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.retrieve()
            >>> dr.save()
        '''
        
        self.path = ''
        
        return self        
        
    def id(self, ID :int):
        '''
        Returns dana-8 classification with matching id
        Not yet working

        Args:
            id (INT): The dana-8 id.

        Returns:
            self: The DanaRetriver object.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.id(2)
            >>> dr.save()
        '''
        
        id = str(ID)
        
        self.path = '/' + id
        
        return self
    
    def groups(self):
        '''
        Returns Dana 8th edition group classifications.

        Returns:
            self: The DanaRetriever object.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.groups()
            >>> dr.save()
        '''
        
        self.path = '/groups'
        
        return self
    
    def subgroups(self):
        '''
        Returns Dana 8th edition subgroup classifications.

        Returns:
            self: The DanaRetriever object.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.subgroups()
            >>> dr.save()
        '''

        self.path = '/subgroups'
        
        return self
    
    def saveto(self, OUTDIR=''):
        '''
            Executes the query to retrieve the countries with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved countries will be saved. If not provided, the current directory will be used.

            Returns:
                None

            Example:
                >>> dr = DanaRetriever()
                >>> dr.saveto("/path/to/directory")
        '''
        
        print("Retrieving Dana8 Data. This may take a while... ")

        params = self._params
        outdir = OUTDIR
        end_point = 'dana-8' + self.path
        
        ma = mindat_api.MindatApi()
        ma.get_mindat_list(params, end_point, outdir)

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()
    
    def save(self):
        '''
            Executes the query to retrieve the list of geomaterials and saves the results to the current directory.

            Returns:
                None

            Example:
                >>> cr = contriesRetriever()
                >>> cr.save()
        '''
        self.saveto()


if __name__ == '__main__':
    dr = DanaRetriever()
    dr.groups().save()
