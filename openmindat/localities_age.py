from . import (
    mindat_api,  # noqa: F401  (kept: code patches <module>.mindat_api.MindatApi)
)
from ._base import _IdRetriever, _PagedRetriever


class LocalitiesAgeRetriever(_PagedRetriever):
    """
    A class to facilitate the retrieval of locality data from the Mindat API filtered by page.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_age

    Methods:
        page(INT): returns a page of localities.
        saveto(OUTDIR, FILENAME): Executes the search query and saves the data to a specified directory.
        save(FILENAME): Executes the search query and saves the data to the current directory.

    Usage:
        >>> lar = LocalitiesAgeRetriever()
        >>> lar.page(2).save()

    Press q to quit.
    """
    
    BASE_ENDPOINT = 'v1/locality-age'


class LocalitiesAgeIdRetriever(_IdRetriever):
    """
    A class to facilitate the retrieval of locality data from the Mindat API filtered by id.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_age/operation/locality_age_retrieve

    Methods:
        id(INT): returns the country with the matching id.
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

    Usage:
        >>> lair = LocalitiesAgeIdRetriever()
        >>> lair.id(5).save()

    Press q to quit.
    """

    BASE_ENDPOINT = 'v1/locality-age'


if __name__ == '__main__':
    lair = LocalitiesAgeIdRetriever()
    lair.id(3).save()
