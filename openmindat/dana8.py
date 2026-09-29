from . import (
    mindat_api,  # noqa: F401  (kept: code patches <module>.mindat_api.MindatApi)
)
from ._base import _R, _IdRetriever

#todo: Check back in when retrieve and id functions are implemented


class DanaRetriever(_IdRetriever):
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
    
    BASE_ENDPOINT = 'v1/dana-8'
    _SUB_LISTING_HINT = (
        "DanaRetriever needs a sub-listing: the Mindat API has no plain list at /dana-8/. Call .groups(), .subgroups() or .id(<id>) before get_dict()/save()."
    )
    _ENDPOINT_STYLE = "join_if_sub"

    def retrieve(self: _R) -> _R:
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
        
    def groups(self: _R) -> _R:
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
    
    def subgroups(self: _R) -> _R:
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


if __name__ == '__main__':
    dr = DanaRetriever()
    dr.groups().save()
