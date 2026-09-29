from . import (
    mindat_api,  # noqa: F401  (kept: code patches <module>.mindat_api.MindatApi)
)
from ._base import _as_int, _BaseRetriever


class GeomaterialSearchRetriever(_BaseRetriever):
    """
    A class to facilitate the retrieval of geomaterial data from the Mindat API using search keywords. It enables users to construct queries based on specific keywords and offers functionality to save the retrieved data.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/geomaterials_search

    Methods:
        geomaterials_search(KEYWORDS): Updates the search query with specified keywords.
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

    Usage:
        >>> gsr = GeomaterialSearchRetriever()
        >>> gsr.geomaterials_search("quartz, green, hexagonal").save()

    Press q to quit.
    """

    BASE_ENDPOINT = 'v1/geomaterials-search'
    
    def geomaterials_search(self, KEYWORDS):
        '''
        Updates the query parameters to search for geomaterials based on specified keywords.

        Args:
            KEYWORDS (str): A string containing the keywords to search for. 

        Returns:
            self: The GeomaterialRetriever object, allowing for method chaining.

        Example:
            >>> gsr = GeomaterialSearchRetriever()
            >>> gsr.geomaterials_search("quartz, green, hexagonal")
            >>> gsr.save()
        '''
        keywords = KEYWORDS
        self._params.update({'q': keywords})
        return self

    def e(self, EXACT):
        '''
        Returns only exact name matches when set to 1 (or True).

        Args:
            EXACT (int or bool): 1/True for exact matches only, 0/False for all matches.

        Returns:
            self: The GeomaterialSearchRetriever object.

        Example:
            >>> gsr = GeomaterialSearchRetriever()
            >>> gsr.geomaterials_search("quartz").e(1).get_dict()
        '''
        self._params.update({"e": _as_int(EXACT, "EXACT")})
        return self

    def ima(self, IMA):
        '''
        Returns only IMA-approved minerals when set to 1 (or True).

        Args:
            IMA (int or bool): 1/True for IMA-approved minerals only.

        Returns:
            self: The GeomaterialSearchRetriever object.

        Example:
            >>> gsr = GeomaterialSearchRetriever()
            >>> gsr.geomaterials_search("quartz").ima(1).get_dict()
        '''
        self._params.update({"ima": _as_int(IMA, "IMA")})
        return self

    def size(self, SIZE):
        '''
        Limits the number of records when a fuzzy search applies (Mindat API default: 12).

        Args:
            SIZE (int): Maximum number of fuzzy-search records.

        Returns:
            self: The GeomaterialSearchRetriever object.

        Example:
            >>> gsr = GeomaterialSearchRetriever()
            >>> gsr.geomaterials_search("quarz").size(5).get_dict()
        '''
        self._params.update({"size": _as_int(SIZE, "SIZE")})
        return self


if __name__ == '__main__':
    gsr = GeomaterialSearchRetriever()
    gsr.geomaterials_search("quartz, green, hexagonal").save()
