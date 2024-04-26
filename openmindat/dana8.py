from . import mindat_api

#todo: Check back in when retrieve and id functions are implemented

class DanaRetriever:
    """
    A class to facilitate the retrieval of dana-8 data from the Mindat API filtering with type of groups or subgroups.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/dana-8/operation/dana_8_retrieve
    
    This class allows for method chaining but if more than one method is used it will only return data for the last method used.

    Methods:
        retrieve: N/A
        id: N/A
        groups: returns group information
        subgroups: returns subgroup information

    Usage:
        >>> dr = DanaRetriever()
        >>> dr.groups().save()

    Press q to quit.
    """
    
    def __init__(self):
        self.sub_endpoint = ''
        self.end_point = 'dana-8'
        
        self._params = {}
        self._init_params()
    
    def _init_params(self):
        self.end_point = 'dana-8'
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
            self: The DanaRetriever object.

        Example:
            >>> dr = DanaRetriever()
            >>> dr.page_size(1500)
            >>> dr.save()

        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
        
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
        
        self.sub_endpoint = ''
        
        return self        
        
    def id(self, ID):
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
        try:
            ID = int(ID)
        except ValueError:
            raise ValueError("Invalid input. ID must be a valid integer.")
        
        id = str(ID)
        
        self.sub_endpoint = id
        
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
        
        self.sub_endpoint = 'groups'
        
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

        self.sub_endpoint = 'subgroups'
        
        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the dana-8 data with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved dana-8 data will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> dr = DanaRetriever()
                >>> dr.saveto("/path/to/directory")
        '''
        
        params = self._params
        outdir = OUTDIR
        file_name = FILE_NAME
        end_point = self.end_point
        
        if self.sub_endpoint != '':
            end_point = '/'.join(['dana-8', self.sub_endpoint])
        
        ma = mindat_api.MindatApi()
        
        if self.sub_endpoint.isnumeric():
            ma.download_mindat_json(params, end_point, outdir, file_name)
        else:
            ma.download_mindat_json(params, end_point, outdir, file_name)

        # Reset the query parameters in case the user wants to make another query.
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of dana-8 data and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> dr = DanaRetriever()
                >>> dr.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve the dana-8 data as a dictionary.

        Returns:
            list of dictionaries.

        Example:
            >>> dr = danaRetriever()
            >>> danaGroups = cr.group().get_dict()

        '''
       
        params = self._params        
        
        if self.sub_endpoint != '':
            end_point = '/'.join(['dana-8', self.sub_endpoint])
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
        
        self._init_params()
        return results


if __name__ == '__main__':
    dr = DanaRetriever()
    dr.groups().save()
