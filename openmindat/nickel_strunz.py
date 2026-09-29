from . import (
    mindat_api,  # noqa: F401  (kept: code patches <module>.mindat_api.MindatApi)
)
from ._base import _IdRetriever

#todo: Check back in when retrieve and id functions are implemented


class StrunzRetriever(_IdRetriever):
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

    BASE_ENDPOINT = 'v1/nickel-strunz-10'
    _SUB_LISTING_HINT = (
        "StrunzRetriever needs a sub-listing: the Mindat API has no plain list at /nickel-strunz-10/. Call .classes(), .subclasses(), .families() or .id(<id>) before get_dict()/save()."
    )
    
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


if __name__ == '__main__':
    sr = StrunzRetriever()
    sr.classes().save()
