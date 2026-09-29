from . import (
    mindat_api,  # noqa: F401  (kept: code patches <module>.mindat_api.MindatApi)
)
from ._base import _IdRetriever, _PagedRetriever


class LocalitiesTypeRetriever(_PagedRetriever):
    """
    A class to facilitate the retrieval of locolity data from the Mindat API filtered by page.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_type

    Methods:
        page(INT): returns a page of localities.
        saveto(OUTDIR, FILENAME): Executes the search query and saves the data to a specified directory.
        save(FILENAME): Executes the search query and saves the data to the current directory.

    Usage:
        >>> ltr = LocalitiesTypeRetriever()
        >>> ltr.page(2).save()

    Press q to quit.
    """

    BASE_ENDPOINT = 'v1/locality-type'   


class LocalitiesTypeIdRetriever(_IdRetriever):
    """
    A class to facilitate the retrieval of locality data from the Mindat API filtered by id.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/locality_type/operation/locality_type_retrieve

    Methods:
        id(INT): returns the country with the matching id.
        saveto(OUTDIR): Executes the search query and saves the data to a specified directory.
        save(): Executes the search query and saves the data to the current directory.

    Usage:
        >>> ltir = LocalitiesTypeIdRetriever()
        >>> ltir.id(5).save()

    Press q to quit.
    """

    BASE_ENDPOINT = 'v1/locality-type'   


if __name__ == '__main__':
    ltir = LocalitiesTypeIdRetriever()
    ltir.id(2).save()
