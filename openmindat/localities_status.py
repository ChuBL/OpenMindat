from . import (
    mindat_api,  # noqa: F401  (kept: code patches <module>.mindat_api.MindatApi)
)
from ._base import _IdRetriever, _PagedRetriever


class LocalitiesStatusRetriever(_PagedRetriever):
    """
    A class to facilitate the retrieval of locality data from the Mindat API filtered by page.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_status

    Methods:
        page(INT): returns a page of localities.
        saveto(OUTDIR, FILENAME): Executes the search query and saves the data to a specified directory.
        save(FILENAME): Executes the search query and saves the data to the current directory.

    Usage:
        >>> lsr = LocalitiesStatusRetriever()
        >>> lsr.page(2).save()

    Press q to quit.
    """

    BASE_ENDPOINT = 'v1/locality-status' 


class LocalitiesStatusIdRetriever(_IdRetriever):
    """
    A class to facilitate the retrieval of locality data from the Mindat API filtered by id.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_status/operation/locality_status_retrieve

    Methods:
        id(INT): returns the country with the matching id.
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

    Usage:
        >>> lsir = LocalitiesStatusIdRetriever()
        >>> lsir.id(5).save()

    Press q to quit.
    """

    BASE_ENDPOINT = 'v1/locality-status'  


if __name__ == '__main__':
    lsir = LocalitiesStatusIdRetriever()
    lsir.id(2).save()
