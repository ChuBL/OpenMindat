from datetime import date, datetime
from typing import Any

from . import (
    mindat_api,  # noqa: F401  (kept: code patches <module>.mindat_api.MindatApi)
)
from ._base import _R, _as_int, _IdRetriever, _PagedRetriever


class LocalityTranslationsRetriever(_PagedRetriever):
    """
    A class to facilitate the retrieval of locality name translations from the Mindat API.
    For more information visit: https://api.mindat.org/v1/schema/redoc/#tag/Localities

    Methods:
        lt_loc(LOCALITY_IDS): translations of these locality ids.
        lt_iso(LANGUAGE): translations in this language code, e.g. "fr".
        lt_text(TEXT): translations whose text contains TEXT.
        lt_important(FLAG): filter on the "important" flag (0 or 1).
        lt_datetime_gte(DATETIME): translations added or changed at or after DATETIME.
        ordering(FIELD): order the results, e.g. "-lt_datetime".
        page(INT), page_size(INT), verbose(INT), get_dict(), save(), saveto()

    Usage:
        >>> ltr = LocalityTranslationsRetriever()
        >>> ltr.lt_loc([14090, 14244]).lt_iso("fr").get_dict()

    Press q to quit.
    """

    BASE_ENDPOINT = 'v1/locality-translations'

    def lt_loc(self: _R, LOCALITY_IDS: int | str | list[int] | tuple[int, ...]) -> _R:
        '''
        Returns translations of the given locality ids.

        Args:
            LOCALITY_IDS (int, str or list[int]): one id, a comma-separated string, or a list.

        Returns:
            self: The LocalityTranslationsRetriever object.

        Example:
            >>> ltr = LocalityTranslationsRetriever()
            >>> ltr.lt_loc([14090, 14244]).get_dict()
        '''
        ids: list[Any]
        if isinstance(LOCALITY_IDS, str):
            ids = [part.strip() for part in LOCALITY_IDS.split(",") if part.strip()]
        elif isinstance(LOCALITY_IDS, (list, tuple, set)):
            ids = list(LOCALITY_IDS)
        else:
            ids = [LOCALITY_IDS]
        if not ids:
            raise ValueError("LOCALITY_IDS must contain at least one locality id.")
        loc_string = ",".join(str(_as_int(i, "LOCALITY_IDS")) for i in ids)
        self._params.update({"lt_loc": loc_string})
        return self

    def lt_iso(self: _R, LANGUAGE: str) -> _R:
        '''
        Returns translations in the given language code.

        Args:
            LANGUAGE (str): language code as stored by Mindat, e.g. "fr", "de", "zh".

        Returns:
            self: The LocalityTranslationsRetriever object.

        Example:
            >>> ltr = LocalityTranslationsRetriever()
            >>> ltr.lt_iso("fr").get_dict()
        '''
        self._params.update({"lt_iso": LANGUAGE})
        return self

    def lt_text(self: _R, TEXT: str) -> _R:
        '''
        Returns translations whose text contains TEXT.

        Args:
            TEXT (str): text to look for.

        Returns:
            self: The LocalityTranslationsRetriever object.

        Example:
            >>> ltr = LocalityTranslationsRetriever()
            >>> ltr.lt_text("Belg").get_dict()
        '''
        self._params.update({"lt_text": TEXT})
        return self

    def lt_important(self: _R, FLAG: int) -> _R:
        '''
        Filters on the translation's "important" flag.

        Args:
            FLAG (int or bool): 1/True or 0/False.

        Returns:
            self: The LocalityTranslationsRetriever object.

        Example:
            >>> ltr = LocalityTranslationsRetriever()
            >>> ltr.lt_important(1).get_dict()
        '''
        self._params.update({"lt_important": _as_int(FLAG, "FLAG")})
        return self

    def lt_datetime_gte(self: _R, DATETIME: str | datetime | date) -> _R:
        '''
        Returns translations added or changed at or after DATETIME.

        Args:
            DATETIME (str, datetime or date): "YYYY-MM-DD HH:MM:SS", or a datetime/date object.

        Returns:
            self: The LocalityTranslationsRetriever object.

        Example:
            >>> ltr = LocalityTranslationsRetriever()
            >>> ltr.lt_datetime_gte("2024-01-01 00:00:00").get_dict()
        '''
        if isinstance(DATETIME, datetime):
            value = DATETIME.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(DATETIME, date):
            value = DATETIME.strftime("%Y-%m-%d 00:00:00")
        elif isinstance(DATETIME, str):
            try:
                # Format check only; the Mindat API takes a naive "YYYY-MM-DD HH:MM:SS" string.
                datetime.strptime(DATETIME, "%Y-%m-%d %H:%M:%S")  # noqa: DTZ007
            except ValueError:
                raise ValueError(
                    f"DATETIME must look like 'YYYY-MM-DD HH:MM:SS', got {DATETIME!r}"
                ) from None
            value = DATETIME
        else:
            # ValueError for every invalid argument, as elsewhere in openmindat (D9).
            raise ValueError(f"DATETIME must be a string, datetime or date, got {DATETIME!r}")  # noqa: TRY004
        self._params.update({"lt_datetime_gte": value})
        return self

    def ordering(self: _R, ORDERING: str) -> _R:
        '''
        Orders the results by a field; prefix with "-" for descending order.

        Args:
            ORDERING (str): e.g. "lt_datetime" or "-lt_datetime".

        Returns:
            self: The LocalityTranslationsRetriever object.

        Example:
            >>> ltr = LocalityTranslationsRetriever()
            >>> ltr.ordering("-lt_datetime").page_size(10).page(1).get_dict()
        '''
        self._params.update({"ordering": ORDERING})
        return self


class LocalityTranslationsIdRetriever(_IdRetriever):
    """
    A class to facilitate the retrieval of one locality name translation by its id (lt_id).
    For more information visit: https://api.mindat.org/v1/schema/redoc/#tag/Localities

    Methods:
        id(INT): the translation id (lt_id).
        get_dict(), save(), saveto(), verbose(INT)

    Usage:
        >>> ltir = LocalityTranslationsIdRetriever()
        >>> ltir.id(2).get_dict()

    Press q to quit.
    """

    BASE_ENDPOINT = 'v1/locality-translations'
