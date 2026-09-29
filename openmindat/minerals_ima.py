from datetime import datetime

from . import (
    mindat_api,  # noqa: F401  (kept: code patches <module>.mindat_api.MindatApi)
)
from ._base import _R, _IdRetriever, _PagedRetriever
from .geomaterials import GeomaterialRetriever as _GeomaterialRetriever


class MineralsIMARetriever(_PagedRetriever):
    '''
    A class for querying mineral data from the Mindat API. It supports various query parameters such as mineral IDs, IMA status, fields selection, and pagination. The class enables method chaining for building complex queries and provides functionalities to save the queried data either to a specified directory or the current directory.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/minerals_ima

    Usage:
        >>> mir = MineralsIMARetriever()
        >>> mir.ima(1).fields("id,name,ima_formula").saveto("/path/to/directory")

    Press q to quit.
    '''

    BASE_ENDPOINT = 'v1/minerals-ima'

    def expand(self: _R, EXPAND_FIELDS: str | list[str]) -> _R:
        '''
        Expand the query to include related minerals and select specific fields to expand.

        Args:
            EXPAND_FIELDS(list[str] or str): The fields to expand. Valid options are:
                - "description"
                - "type_localities"
                - "locality"
                - "relations"
                - "minstats"
                - "~all" (expand all fields)
                - "*" (expand all fields)

        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.expand(["description", "type_localities"])
            >>> mir.saveto()
        '''

        valid_options = ["description", "type_localities", "locality", "relations", "minstats", "~all", "*"]

        if isinstance(EXPAND_FIELDS, str):
            EXPAND_FIELDS = [EXPAND_FIELDS]

        invalid_options = [field for field in EXPAND_FIELDS if field not in valid_options]

        if invalid_options:
            print(f"Possible Invalid EXPAND_FIELDS: {', '.join(invalid_options)}\nPlease refer to https://api.mindat.org/schema/redoc/#tag/minerals_ima")

        expand_fields = EXPAND_FIELDS
        self._params.update({
            'expand': expand_fields
        })

        return self
    
    def fields(self: _R, FIELDS: str) -> _R:
        '''
        Specify the selected fields to be retrieved for each geomaterial.
        Please check the API documentation for the list of available fields.
        https://api.mindat.org/schema/redoc/#tag/minerals_ima/operation/minerals_ima_list

        Args:
            FIELDS (str): The selected fields to be retrieved. Multiple fields should be separated by commas.

        Example Input:
            fields=id,name,ima_formula,ima_symbol,ima_year,discovery_year,ima_status,ima_notes,type_specimen_store,mindat_longid,mindat_guid,type_localities,description_short,mindat_formula,mindat_formula_note,~all,*
        Returns:
            self: The MineralsIMARetriever object.
        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.fields("id,name,ima_formula")
            >>> mir.saveto()
        '''

        self._params.update({
            'fields': FIELDS
        })

        return self
    
    def id_in(self: _R, ID_IN_LIST: str) -> _R:
        '''
        Set the IDs for the query.

        Args:
            ID_IN_LIST (str): The IDs to filter the query, separated by commas.

        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.id_in("123,456,789")
            >>> mir.saveto()
        '''

        ids = str(ID_IN_LIST)

        self._params.update({
            'id_in': ids
        })

        return self

    def ima(self: _R, IS_IMA: bool | int) -> _R:
        '''
            This filter is probably not working as intended. Just ignore it for now.
            Include IMA-approved names only (1) / to be determined(0)
            
            Args:
                IS_IMA (int, bool): The IMA status to filter the query.
                                1/True for IMA-approved names only,
                                0/False for to be determined.
            
            Returns:
                self: The MineralsIMARetriever object.
            
            Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.ima(1)        # Using int
            >>> mir.ima(True)     # Using bool
            >>> mir.ima(False)    # Using bool
            >>> mir.saveto()
        '''
        
        if IS_IMA in [0, 1, True, False]:
            ima_value = bool(IS_IMA)
        else:
            raise ValueError(f"Invalid IS_IMA: {IS_IMA}\nIS_IMA must be 0, 1, True, or False.")
        
        self._params.update({
            'ima': ima_value
        })
        
        return self
    
    def omit(self: _R, OMIT_FIELDS: str) -> _R:
        '''
        Set the fields to omit from the query.

        Args:
            OMIT_FIELDS (str): The fields to omit, separated by commas. 
            Please check the API documentation for the list of available fields.
            https://api.mindat.org/schema/redoc/#tag/minerals_ima/operation/minerals_ima_list
        Returns:
            self: The MineralsIMARetriever object.
            
        Valid options:
            id,name,ima_formula,ima_symbol,ima_year,discovery_year,ima_status,ima_notes,type_specimen_store,mindat_longid,mindat_guid,type_localities,description_short,mindat_formula,mindat_formula_note,~all,*

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.omit("id,name")
            >>> mir.saveto()
        '''

        omit_fields = OMIT_FIELDS
        self._params.update({
            'omit': omit_fields
        })

        return self
    
    def q(self: _R, SEARCHING_KEYWORDS: str) -> _R:
        '''
        Sets the keywords to search for.

        Args:
            SEARCHING_KEYWORDS (str): The keywords to search for.

        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.q("quartz")
            >>> mir.saveto()
        '''
        self._params.update({
            'q': SEARCHING_KEYWORDS
        })

        return self
    
    def updated_at(self: _R, DATE_STR: str) -> _R:
        '''	
            Sets the last updated datetime for the geomaterial query.

            Args:
                DATE_STR (str): The last updated datetime in the format %Y-%m-%d %H:%M:%S.

            Returns:
                self: The MineralsIMARetriever object.

            Raises:
                ValueError: If the provided DATE_STR is not a valid datetime string.

            Example:
                >>> retriever = GeomaterialRetriever()
                >>> retriever.updated_at('2022-01-01 12:00:00')
                >>> retriever.save()
        '''
        try:
            datetime.strptime(DATE_STR, '%Y-%m-%d %H:%M:%S')  # noqa: DTZ007  (format check only)
        except ValueError:
            raise ValueError("Invalid datetime format. Please provide the datetime in the format %Y-%m-%d %H:%M:%S.")

        self._params.update({
            'updated_at': DATE_STR
        })

        return self

    # Filters shared with /geomaterials/: the Mindat OpenAPI schema defines them identically on
    # /minerals-ima/, so the GeomaterialRetriever implementations are reused as-is.
    bi_max = _GeomaterialRetriever.bi_max
    bi_min = _GeomaterialRetriever.bi_min
    cleavagetype = _GeomaterialRetriever.cleavagetype
    colour = _GeomaterialRetriever.colour
    crystal_system = _GeomaterialRetriever.crystal_system
    density_max = _GeomaterialRetriever.density_max
    density_min = _GeomaterialRetriever.density_min
    diapheny = _GeomaterialRetriever.diapheny
    el_essential = _GeomaterialRetriever.el_essential
    el_exc = _GeomaterialRetriever.el_exc
    el_inc = _GeomaterialRetriever.el_inc
    entrytype = _GeomaterialRetriever.entrytype
    fracturetype = _GeomaterialRetriever.fracturetype
    groupid = _GeomaterialRetriever.groupid
    hardness_max = _GeomaterialRetriever.hardness_max
    hardness_min = _GeomaterialRetriever.hardness_min
    id_max = _GeomaterialRetriever.id_max
    id_min = _GeomaterialRetriever.id_min
    ima_notes = _GeomaterialRetriever.ima_notes
    ima_status = _GeomaterialRetriever.ima_status
    lustretype = _GeomaterialRetriever.lustretype
    meteoritical_code = _GeomaterialRetriever.meteoritical_code
    meteoritical_code_exists = _GeomaterialRetriever.meteoritical_code_exists
    name = _GeomaterialRetriever.name
    non_utf = _GeomaterialRetriever.non_utf
    optical2v_max = _GeomaterialRetriever.optical2v_max
    optical2v_min = _GeomaterialRetriever.optical2v_min
    opticalsign = _GeomaterialRetriever.opticalsign
    opticaltype = _GeomaterialRetriever.opticaltype
    polytypeof = _GeomaterialRetriever.polytypeof
    ri_max = _GeomaterialRetriever.ri_max
    ri_min = _GeomaterialRetriever.ri_min
    streak = _GeomaterialRetriever.streak
    synid = _GeomaterialRetriever.synid
    tenacity = _GeomaterialRetriever.tenacity
    varietyof = _GeomaterialRetriever.varietyof
    color = _GeomaterialRetriever.color
    diaphaneity = _GeomaterialRetriever.diaphaneity
    elements_exc = _GeomaterialRetriever.elements_exc
    elements_inc = _GeomaterialRetriever.elements_inc


class MineralsIdRetriever(_IdRetriever):
    """
    This module provides the MineralsIdRetriever class for returning Minerals by id
    For more information visit: https://api.mindat.org/schema/redoc/#tag/minerals_ima/operation/minerals_ima_retrieve

    Usage:
        >>> midr = MineralsIdRetriever()
        >>> midr.id(5)

    Attributes:
        id (int): An int to store id parameter.
    """
    
    BASE_ENDPOINT = 'v1/minerals-ima'


if __name__ == '__main__':
    mir = MineralsIMARetriever()
    mir.ima(1).saveto()
