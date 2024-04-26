from . import mindat_api
from datetime import datetime

class GeomaterialRetriever:
    """
    This module provides the GeomaterialRetriever class for retrieving geomaterial data from the Mindat API. This class offers various methods to specify query parameters for filtering and retrieving detailed information about geomaterials, such as minerals and rocks.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/geomaterials

    The class allows for setting parameters like birifrigence, cleavage type, color, crystal system, density, diaphaneity, chemical elements inclusion or exclusion, entry types, optical properties, and more. It provides flexibility through method chaining and supports saving the query results either to a specified directory or to the current directory.

    Usage:
        >>> gr = GeomaterialRetriever()
        >>> gr.cleavagetype('Distinct/Good').colour('blue').crystal_system(["Amorphous", "Hexagonal"]).save()
        >>> gr.density_max('9').density_min(8).save()

    Press q to quit.
    """
    
    def __init__(self) -> None:
        self.end_point = 'geomaterials'
        self._params = {}
        self._init_params()
         # Flag to indicate if the geomaterials have been retrieved

    def _init_params(self):
        self.end_point = 'geomaterials'
        self._params.clear()
        self._params.update({'format': 'json'})
        self.page_size(1500)

    def bi_min(self, MIN):
        '''
        Sets the minimum value of birifrigence for filtering minerals.

        Args:
            MIN (str): The minimum value of birifrigence.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.bi_min("0.01")
            >>> gr.save()
        '''

        self._params.update({
            'bi_min': str(MIN)
        })

        return self

    def bi_max(self, MAX):
        '''
        Sets the maximum value of birifrigence for filtering minerals.

        Args:
            MAX (str): The maximum value of birifrigence.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.bi_max("0.05")
            >>> gr.save()
        '''

        self._params.update({
            'bi_max': str(MAX)
        })

        return self
    
    def cleavagetype(self, CLEAVAGETYPE):
        '''
        Sets the cleavage type for filtering minerals.

        Args:
            CLEAVAGETYPE (str or list[str] or None): The cleavage types. Can be a string or a list of the following values:
                - "Distinct/Good": Indicates distinct or good cleavage.
                - "Imperfect/Fair": Indicates imperfect or fair cleavage.
                - "None Observed": Indicates no observed cleavage.
                - "Perfect": Indicates perfect cleavage.
                - "Poor/Indistinct": Indicates poor or indistinct cleavage.
                - "Very Good": Indicates very good cleavage.
                If None is provided, the cleavage type filter will be removed.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.cleavagetype("Perfect")
            >>> gr.save()

        '''

        if isinstance(CLEAVAGETYPE, str):
            cleavage_types = [CLEAVAGETYPE]
        else:
            cleavage_types = CLEAVAGETYPE
        
        if cleavage_types is not None:
            valid_cleavage_types = ["Distinct/Good", "Imperfect/Fair", "None Observed", "Perfect", "Poor/Indistinct", "Very Good"]
            invalid_cleavage_types = [ct for ct in cleavage_types if ct not in valid_cleavage_types]
            if invalid_cleavage_types:
                raise ValueError(f"Invalid cleavage types: {', '.join(invalid_cleavage_types)}. Valid options are: {', '.join(valid_cleavage_types)}")
            self._params.update({
                'cleavage_type': cleavage_types
            })
        else:
            self._params.update({
                'cleavage_type': None
            })
        
        return self
    
    def colour(self, COLOUR):
        '''
        Sets the colour for filtering minerals.

        Args:
            COLOR (str): The colours.
                If None is provided, the colour filter will be removed.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.colour("green")
            >>> gr.save()

        '''
        
        colour = COLOUR
        if colour is not None:
            self._params.update({
                'colour': colour
            })
        else:
            self._params.update({
                'colour': None
            })
        
        return self
    
    def color(self, COLOR):
        '''
        Sets the color for filtering minerals.

        Args:
            COLOR (str): The colors.
                If None is provided, the color filter will be removed.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.color("green")
            >>> gr.save()

        '''
        
        return self.colour(COLOR)
    
    def crystal_system(self, CRYSTAL_SYSTEM):
        '''
        Sets the crystal system for filtering minerals.
        Crystal system (csystem): multiple choice (OR)

        Args:
            CRYSTAL_SYSTEM (str or list[str] or None): The crystal systems to filter by. Can be a string or a list of the following values:
                "Amorphous", "Hexagonal", "Icosahedral", "Isometric", "Monoclinic", "Orthorhombic", "Tetragonal", "Triclinic", "Trigonal".

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.crystal_system("Hexagonal")
            >>> gr.save()

        '''

        if isinstance(CRYSTAL_SYSTEM, str):
            crystal_systems = [CRYSTAL_SYSTEM]
        else:
            crystal_systems = CRYSTAL_SYSTEM
        
        if crystal_systems is not None:
            valid_crystal_systems = ["Amorphous", "Hexagonal", "Icosahedral", "Isometric", "Monoclinic", "Orthorhombic", "Tetragonal", "Triclinic", "Trigonal"]
            invalid_crystal_systems = [cs for cs in crystal_systems if cs not in valid_crystal_systems]
            if invalid_crystal_systems:
                raise ValueError(f"Invalid crystal system(s) found: {', '.join(invalid_crystal_systems)}. Valid options are: {', '.join(valid_crystal_systems)}")
            self._params.update({
                'crystal_system': crystal_systems
            })
        else:
            self._params.update({
                'crystal_system': None
            })
        
        return self
    
    def density_max(self, MAX):
        '''
        Density measured, to (dmeas<=).
        Get all minerals with density less than or equal to MAX.
        
        Args:
            MAX (float): The maximum value of density.
            
        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.density_max(5.0)
            >>> gr.save()

        '''

        density_max = float(MAX)
        self._params.update({
            'density_max': density_max
        })
        
        return self
    
    def density_min(self, MIN):
        '''
        Density measured, from (dmeas2>=).
        Get all minerals with density greater than or equal to MIN.
        
        Args:
            MIN (float): The minimum value of density.
            
        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.density_min(2.0)
            >>> gr.save()

        '''

        density_min = float(MIN)
        self._params.update({
            'density_min': density_min
        })
        
        return self
    
    def diaphaneity(self, DIAPHANEITY):
        '''
        Diaphaneity (transparency): multiple choice (AND)

        Args:
            DIAPHANEITY (str or list[str]): The diaphaneity options. Can be a string or a list of strings representing the diaphaneity options. Valid options are "Opaque", "Translucent", and "Transparent".

        Returns:
            self: The GeomaterialRetriever object.
        
        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.diaphaneity("Transparent")
            >>> gr.save()

        '''

        if isinstance(DIAPHANEITY, str):
            diaphaneity_options = [DIAPHANEITY]
        else:
            diaphaneity_options = DIAPHANEITY

        valid_options = ["Opaque", "Translucent", "Transparent"]
        invalid_options = [option for option in diaphaneity_options if option not in valid_options]

        if invalid_options:
            raise ValueError(f"Invalid diaphaneity options: {', '.join(invalid_options)}\nValid options are: {', '.join(valid_options)}")

        self._params.update({
            'diaphaneity': diaphaneity_options
        })

        return self
    
    def elements_exc(self, ELEMENTS_EXC):
        '''
        Exclude chemical elements.

        Args:
            ELEMENTS_EXC (str): Comma-separated string of chemical elements to exclude.

        Returns:
            self: The GeomaterialRetriever object.
        
        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.elements_exc("Au,Ag")
            >>> gr.save()

        '''

        elements_exc = ELEMENTS_EXC
        self._params.update({
            'elements_exc': elements_exc
        })

        return self
    
    def elements_inc(self, ELEMENTS_INC):
        '''
        Include chemical elements.

        Args:
            ELEMENTS_INC (str): Comma-separated string of chemical elements to include.

        Returns:
            self: The GeomaterialRetriever object.
        
        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.elements_inc("Fe,Cu")
            >>> gr.save()

        '''

        elements_inc = ELEMENTS_INC
        self._params.update({
            'elements_inc': elements_inc
        })

        return self
    
    def entrytype(self, ENTRYTYPE):
        '''
        Set the entry type for the query.

        Args:
            ENTRYTYPE (int or list[int]): The entry type(s) to filter the query. Valid options are:
                0 - mineral
                1 - synonym
                2 - variety
                3 - mixture
                4 - series
                5 - grouplist
                6 - polytype
                7 - rock
                8 - commodity

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.entrytype(0)  # 0 for mineral
            >>> gr.save()

        '''

        if isinstance(ENTRYTYPE, int):
            entry_type = [ENTRYTYPE]
        elif isinstance(ENTRYTYPE, list) and all(isinstance(item, int) for item in ENTRYTYPE):
            entry_type = ENTRYTYPE
        else:
            valid_options = ["0 - mineral", "1 - synonym", "2 - variety", "3 - mixture", "4 - series", "5 - grouplist", "6 - polytype", "7 - rock", "8 - commodity"]
            raise ValueError(f"Invalid ENTRYTYPE: {ENTRYTYPE}\nENTRYTYPE must be an integer or a list of integers: {', '.join(valid_options)}")

        self._params.update({
            'entry_type': entry_type
        })

        return self
    
    def expand(self, EXPAND_FIELDS):
        '''
        Expand the query to include related minerals and select specific fields to expand.

        Args:
            EXPAND_FIELDS (str or list[str]): The fields to expand. Valid options are:
                - "description"
                - "type_localities"
                - "locality"
                - "relations"
                - "minstats"
                - "~all" (expand all fields)
                - "*" (expand all fields)

        Returns:
            self: The GeomaterialRetriever object.
        
        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.expand("description")
            >>> gr.save()

        '''

        if isinstance(EXPAND_FIELDS, str):
            expand_fields = [EXPAND_FIELDS]
        elif isinstance(EXPAND_FIELDS, list):
            expand_fields = EXPAND_FIELDS
        else:
            raise ValueError("Invalid EXPAND_FIELDS: must be a string or a list of strings")

        valid_options = ["description", "type_localities", "locality", "relations", "minstats", "~all", "*"]
        invalid_options = [field for field in expand_fields if field not in valid_options]

        if invalid_options:
            raise ValueError(f"Invalid EXPAND_FIELDS: {', '.join(invalid_options)}\nEXPAND_FIELDS must be one or more of the following: {', '.join(valid_options)}")

        self._params.update({
            'expand': expand_fields
        })

        return self

    def fields(self, FIELDS):
        '''
        Specify the selected fields to be retrieved for each geomaterial.
        Please check the API documentation for the list of available fields.
        https://api.mindat.org/schema/redoc/#tag/geomaterials/operation/geomaterials_list

        Args:
            FIELDS (str): The selected fields to be retrieved. Multiple fields should be separated by commas.

        Example Input:
            fields = "id,longid,guid,name,updttime,mindat_formula,mindat_formula_note,ima_formula,ima_status,ima_notes,varietyof,synid,polytypeof,groupid,entrytype,entrytype_text,description_short,impurities,elements,sigelements,tlform,cim,occurrence,otheroccurrence,industrial,discovery_year,diapheny,cleavage,parting,tenacity,colour,csmetamict,opticalextinction,hmin,hardtype,hmax,vhnmin,vhnmax,vhnerror,vhng,vhns,luminescence,lustre,lustretype,aboutname,other,streak,csystem,cclass,spacegroup,a,b,c,alpha,beta,gamma,aerror,berror,cerror,alphaerror,betaerror,gammaerror,va3,z,dmeas,dmeas2,dcalc,dmeaserror,dcalcerror,cleavagetype,fracturetype,morphology,twinning,epitaxidescription,opticaltype,opticalsign,opticalalpha,opticalbeta,opticalgamma,opticalomega,opticalepsilon,opticalalpha2,opticalbeta2,opticalgamma2,opticalepsilon2,opticalomega2,opticaln,opticaln2,optical2vcalc,optical2vmeasured,optical2vcalc2,optical2vmeasured2,opticalalphaerror,opticalbetaerror,opticalgammaerror,opticalomegaerror,opticalepsilonerror,opticalnerror,optical2vcalcerror,optical2vmeasurederror,opticaldispersion,opticalpleochroism,opticalpleochorismdesc,opticalbirefringence,opticalcomments,opticalcolour,opticalinternal,opticaltropic,opticalanisotropism,opticalbireflectance,opticalr,uv,ir,magnetism,type_specimen_store,commenthard,cim,strunz10ed1,strunz10ed2,strunz10ed3,strunz10ed4,dana8ed1,dana8ed2,dana8ed3,dana8ed4,thermalbehaviour,commentluster,commentbreak,commentdense,commentcrystal,commentcolor,electrical,tranglide,nolocadd,specdispm,spacegroupset,approval_year,publication_year,ima_history,rock_parent,rock_parent2,rock_root,rock_bgs_code,meteoritical_code,key_elements,shortcode_ima,rimin,rimax,weighting,~all,*"
        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.fields("id,name,ima_formula")
            >>> gr.save()

        '''

        self._params.update({
            'fields': FIELDS
        })

        return self
    
    def fracturetype(self, FRACTURETYPE):
        '''
        Fracture type: multiple choice (AND)

        Args:
            FRACTURETYPE (str or list[str] or None): The fracture types. Can be a string, a list of strings, or None. Valid options are "Conchoidal", "Fibrous", "Hackly", "Irregular/Uneven", "Micaceous", "None observed", "Splintery", "Step-Like", and "Sub-Conchoidal".

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.fracturetype("Conchoidal")
            >>> gr.save()

        '''

        if FRACTURETYPE is None:
            fracture_types = None
        elif isinstance(FRACTURETYPE, str):
            fracture_types = [FRACTURETYPE]
        else:
            fracture_types = FRACTURETYPE

        valid_options = ["Conchoidal", "Fibrous", "Hackly", "Irregular/Uneven", "Micaceous", "None observed", "Splintery", "Step-Like", "Sub-Conchoidal"]
        invalid_options = [option for option in fracture_types if option not in valid_options]

        if invalid_options:
            raise ValueError(f"Invalid fracture types: {', '.join(invalid_options)}\nValid options are: {', '.join(valid_options)}")

        self._params.update({
            'fracture_type': fracture_types
        })

        return self
    
    def groupid(self, GROUPID):
        '''
        Set the group ID for the query.

        Args:
            GROUPID (int): The group ID to filter the query.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.groupid(12)
            >>> gr.save()

        '''

        if not isinstance(GROUPID, int):
            raise ValueError(f"Invalid GROUPID: {GROUPID}\nGROUPID must be an integer.")

        groupid = GROUPID
        self._params.update({
            'groupid': groupid
        })

        return self
    
    def hardness_max(self, MAX):
        '''
        Hardness.
        get all minerals with hardness less than MAX
        
        Args:
            MAX (float): The maximum value of hardness.
        
        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.hardness_max(7.0)
            >>> gr.save()

        '''

        hardness_max = float(MAX)
        self._params.update({
            'hardness_max': hardness_max
        })
        
        return self
    
    def hardness_min(self, MIN):
        '''
        Hardness.
        get all minerals with hardness greater than MIN
        
        Args:
            MIN (float): The minimum value of hardness.
        
        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.hardness_min(3.0)
            >>> gr.save()

        '''

        hardness_min = float(MIN)
        self._params.update({
            'hardness_min': hardness_min
        })
        
        return self
    
    def id__in(self, ID_IN_STRING):
        '''
        Set the IDs for the query.

        Args:
            ID_IN_STRING (str): The IDs to filter the query, separated by commas.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.id__in("1001,1002,1003")
            >>> gr.save()

        '''

        ids = str(ID_IN_STRING)

        self._params.update({
            'id__in': ids
        })

        return self
    
    def ima(self, IS_IMA):
        '''
        Include IMA-approved names only (true) / exclude IMA-approved (false)

        Args:
            IS_IMA (bool): The IMA status to filter the query.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.ima(True)
            >>> gr.save()

        '''

        if not isinstance(IS_IMA, bool):
            raise ValueError(f"Invalid IS_IMA: {IS_IMA}\nIS_IMA must be a boolean.")

        ima = IS_IMA
        self._params.update({
            'ima': ima
        })

        return self
        
    def ima_notes(self, IMA_NOTES):
        '''
        Set the IMA notes for the query.

        Args:
            IMA_NOTES (list[str]): The IMA notes to filter the query. Possible values are: "GROUP", "INTERMEDIATE", "NAMED_AMPHIBOLE", "PENDING_APPROVAL", "PUBLISHED_WITHOUT_APPROVAL", "REDEFINED", "REJECTED", "RENAMED", "UNNAMED_INVALID", "UNNAMED_VALID".

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.ima_notes(["PENDING_APPROVAL", "REJECTED"])
            >>> gr.save()

        '''
        if IMA_NOTES is None:
            ima_notes = None
        elif isinstance(IMA_NOTES, str):
            ima_notes = [IMA_NOTES]
        elif not isinstance(IMA_NOTES, list):
            raise ValueError(f"Invalid IMA_NOTES: {IMA_NOTES}\nIMA_NOTES must be a list of strings.")
        else:
            ima_notes = IMA_NOTES

        self._params.update({
            'ima_notes': ima_notes
        })

        return self
    
    def ima_status(self, IMA_STATUS):
        '''
        Set the IMA status for the query.

        Args:
            IMA_STATUS (list[str]): The IMA status to filter the query. Possible values are: "APPROVED", "DISCREDITED", "GRANDFATHERED", "PENDING_PUBLICATION", "QUESTIONABLE".

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.ima_status(["APPROVED", "QUESTIONABLE"])
            >>> gr.save()

        '''
        if IMA_STATUS is None:
            ima_status = None
        elif isinstance(IMA_STATUS, str):
            ima_status = [IMA_STATUS]
        elif not isinstance(IMA_STATUS, list):
            raise ValueError(f"Invalid IMA_STATUS: {IMA_STATUS}\nIMA_STATUS must be a list of strings.")
        else:
            ima_status = IMA_STATUS

        self._params.update({
            'ima_status': ima_status
        })

        return self
    
    def lustretype(self, LUSTRETYPE):
        '''
        Set the lustre type for the query.

        Args:
            LUSTRETYPE (list[str]): The lustre types to filter the query. Possible values are: "Adamantine", "Dull", "Earthy", "Greasy", "Metallic", "Pearly", "Resinous", "Silky", "Sub-Adamantine", "Sub-Metallic", "Sub-Vitreous", "Vitreous", "Waxy".

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.lustretype("Metallic")
            >>> gr.save()

        '''
        if LUSTRETYPE is None:
            lustre_type = None
        elif isinstance(LUSTRETYPE, str):
            lustre_type = [LUSTRETYPE]
        elif not isinstance(LUSTRETYPE, list):
            raise ValueError(f"Invalid LUSTRETYPE: {LUSTRETYPE}\nLUSTRETYPE must be a list of strings.")
        else:
            lustre_type = LUSTRETYPE

        self._params.update({
            'lustretype': lustre_type
        })

        return self

    def meteoritical_code(self, METEORITICAL_CODE):
        '''
        Set the meteoritical code for the query.

        Args:
            METEORITICAL_CODE (str): The meteoritical code to filter the query. Supports * and _ as wildcards.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.meteoritical_code("L5")
            >>> gr.save()

        '''
        meteoritical_code = METEORITICAL_CODE
        self._params.update({
            'meteoritical_code': meteoritical_code
        })

        return self

    def meteoritical_code_exists(self, IS_METEORITICAL_CODE_EXISTS): 
        '''	
        Set whether to include geomaterials with meteoritical code or only include empty meteoritical codes.

        Args:
            IS_METEORITICAL_CODE_EXISTS (bool): True to include geomaterials with non-empty meteoritical codes, False to include only empty meteoritical codes.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.meteoritical_code_exists(True)

        '''   
        self._params.update({
            'meteoritical_code_exists': IS_METEORITICAL_CODE_EXISTS
        })

        return self
    
    def name(self, NAME):
        '''
        Set the name for the query.

        Args:
            NAME (str): The name to search for. Supports * and _ as wildcards, e.g. "qu_rtz", "bario*"

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.name("Quartz")
            >>> gr.save()

        '''
        name = NAME
        self._params.update({
            'name': name
        })

        return self
    
    def non_utf(self, IS_NON_UTF):
        '''
        Set whether to include non-UTF mineral names in the query.

        Args:
            IS_NON_UTF (bool): True to include non-UTF mineral names, False to exclude them.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.non_utf(True)
            >>> gr.save()

        '''
        self._params.update({
            'non_utf': IS_NON_UTF
        })

        return self
    
    def omit(self, OMIT_FIELDS):
        '''
        Set the fields to omit from the query.

        Args:
            OMIT_FIELDS (str): The fields to omit, separated by commas. 
            Please check the API documentation for the list of available fields.
            https://api.mindat.org/schema/redoc/#tag/geomaterials/operation/geomaterials_list
        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.omit("id,name")
            >>> gr.save()

        '''

        omit_fields = OMIT_FIELDS
        self._params.update({
            'omit': omit_fields
        })

        return self
    
    def optical2v_max(self, MAX):
        '''
        Optical 2V.
        get all minerals with optical 2V less than MAX
        
        Args:
            MAX (str or float): The maximum value of optical 2V.
        
        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.optical2v_max("60")
            >>> gr.save()

        '''

        if isinstance(MAX, str):
            try:
                MAX = float(MAX)
            except ValueError:
                raise ValueError("Invalid input. MAX must be a valid float or convertible to float.")
        
        optical2v_max = str(MAX)
        self._params.update({
            'optical2v_max': optical2v_max
        })
        
        return self
    
    def optical2v_min(self, MIN):
        '''
        Optical 2V.
        get all minerals with optical 2V greater than MIN
        
        Args:
            MIN (str or float): The minimum value of optical 2V.
        
        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.optical2v_min("30")
            >>> gr.save()

        '''

        if isinstance(MIN, str):
            try:
                MIN = float(MIN)
            except ValueError:
                raise ValueError("Invalid input. MIN must be a valid float or convertible to float.")
        
        optical2v_min = str(MIN)
        self._params.update({
            'optical2v_min': optical2v_min
        })
        
        return self
    
    def opticalsign(self, OPTICALSIGN):
        '''	
        Optical sign: single choice
        
        Args:
            OPTICALSIGN (str): The optical sign of the geomaterial. Valid values are "+", "+/-", "-", or "".
            
        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.opticalsign("+")
            >>> gr.save()

        '''
        valid_options = ["+", "+/-", "-", None]
        
        if OPTICALSIGN not in valid_options:
            raise ValueError(f"Invalid input. OPTICALSIGN must be one of the following: {', '.join(valid_options)}")
        
        self._params.update({
            'opticalsign': OPTICALSIGN
        })
        
        return self
    
    def opticaltype(self, OPTICALTYPE):
        '''
        Sets the optical type of the geomaterial.

        Parameters:
            OPTICALTYPE (str or list): The optical type(s) of the geomaterial. 
                Valid options are "Biaxial", "Isotropic", and "Uniaxial". 
                If a single string is provided, it will be converted to a list.

        Returns:
            self: Returns the instance of the geomaterial object.

        Raises:
            ValueError: If the input OPTICALTYPE is not one of the valid options.
        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.opticaltype("Biaxial")
            >>> gr.save()

        '''
        
        valid_options = ["Biaxial", "Isotropic", "Uniaxial"]
        
        if isinstance(OPTICALTYPE, str):
            OPTICALTYPE = [OPTICALTYPE]  # Convert single string input to list
        
        if not all(opt in valid_options for opt in OPTICALTYPE):
            raise ValueError(f"Invalid input. OPTICALTYPE must be one of the following: {', '.join(valid_options)}")
        
        self._params.update({
            'opticaltype': OPTICALTYPE
        })
        
        return self
    
    def ordering(self, ORDERING):
        '''
        Order the response by a field. Prepend "-" to the field name for descending order.

        Args:
            ORDERING (str): The field name to order the response by. Valid options are "approval_year", "id", "minstats__ms_locentries", "minstats__ms_photos", "name", "updttime", "weighting", "-approval_year", "-id", "-minstats__ms_locentries", "-minstats__ms_photos", "-name", "-updttime", "-weighting".

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.ordering("name")
            >>> gr.save()

        '''
        valid_options = ["approval_year", "id", "minstats__ms_locentries", "minstats__ms_photos", "name", "updttime", "weighting", "-approval_year", "-id", "-minstats__ms_locentries", "-minstats__ms_photos", "-name", "-updttime", "-weighting"]


        if ORDERING not in valid_options:
            raise ValueError(f"Invalid input. ORDERING must be one of the following: {', '.join(valid_options)}")

        self._params.update({
            'ordering': ORDERING
        })

        return self

    def page(self, PAGE):
        '''
        Sets the page number within the paginated result set.

        Args:
            PAGE (int): The page number.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.page(2)
            >>> gr.save()

        '''
        self._params.update({
            'page': PAGE
        })

        return self

    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.page_size(50)
            >>> gr.save()

        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def polytypeof(self, POLYTYPEOF):
        '''
        Sets the polytype of the geomaterial.

        Args:
            POLYTYPEOF (int): The polytype of the geomaterial.

        Returns:
            self: The GeomaterialRetriever object.
        
        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.polytypeof(3)
            >>> gr.save()

        '''
        self._params.update({
            'polytypeof': int(POLYTYPEOF)
        })

        return self
    
    def q(self, SEARCHING_KEYWORDS):
        '''
        Sets the keywords to search for.

        Args:
            SEARCHING_KEYWORDS (str): The keywords to search for.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.q("gemstone")
            >>> gr.save()

        '''
        self._params.update({
            'q': SEARCHING_KEYWORDS
        })

        return self
    
    def ri_max(self, MAX):
        '''
        Sets the maximum refractive index for the geomaterial.

        Args:
            MAX (float): The maximum refractive index.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.ri_max(1.8)
            >>> gr.save()

        '''
        self._params.update({
            'ri_max': float(MAX)
        })

        return self
        
    def ri_min(self, MIN):
        '''
        Sets the minimum refractive index for the geomaterial.

        Args:
            MIN (float): The minimum refractive index.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.ri_min(1.4)
            >>> gr.save()

        '''
        self._params.update({
            'ri_min': float(MIN)
        })

        return self
    
    def streak(self, STREAK):
        '''
        Sets the streak for the geomaterial query.

        Args:
            STREAK (str): The streak of the geomaterial.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.streak("white")
            >>> gr.save()

        '''
        self._params.update({
            'streak': STREAK
        })

        return self
    
    def synid(self, SYNID):
        '''
        Sets the synonym ID for the geomaterial query.

        Args:
            SYNID (int): The synonym ID of the geomaterial.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.synid(123)
            >>> gr.save()

        '''
        self._params.update({
            'synid': SYNID
        })

        return self
    
    def tenacity(self, TENACITY):
        '''
        Sets the tenacity for the geomaterial query.

        Args:
            TENACITY (str or list or None): The tenacity of the geomaterial. Can be a string, a list of strings, or None.
                Valid options for TENACITY:
                - "brittle"
                - "elastic"
                - "flexible"
                - "fragile"
                - "malleable"
                - "sectile"
                - "very brittle"
                - "waxy"

        Returns:
            self: The GeomaterialRetriever object.

        Raises:
            ValueError: If the provided tenacity option is invalid.
            TypeError: If TENACITY is not a string, list, or None.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.tenacity("brittle")
            >>> gr.save()

        '''
        
        valid_options = ["brittle", "elastic", "flexible", "fragile", "malleable", "sectile", "very brittle", "waxy", None]
        if TENACITY is not None:
            if isinstance(TENACITY, str):
                tenacity_list = [TENACITY]  # Convert the string to a list
            elif isinstance(TENACITY, list):
                tenacity_list = TENACITY
            else:
                raise TypeError("TENACITY must be a string, list of string(s), or None")

            for option in tenacity_list:
                if option not in valid_options:
                    raise ValueError(f"Invalid tenacity option: {option}. Valid options are: {', '.join(valid_options)}")

            self._params.update({
                'tenacity': tenacity_list
            })

        return self
    
    def updated_at(self, DATE_STR):
        '''	
            Sets the last updated datetime for the geomaterial query.

            Args:
                DATE_STR (str): The last updated datetime in the format %Y-%m-%d %H:%M:%S.

            Returns:
                self: The GeomaterialRetriever object.

            Raises:
                ValueError: If the provided DATE_STR is not a valid datetime string.

            Example:
                >>> retriever = GeomaterialRetriever()
                >>> retriever.updated_at('2022-01-01 12:00:00')
                >>> retriever.save()
        '''
        try:
            datetime.strptime(DATE_STR, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid datetime format. Please provide the datetime in the format %Y-%m-%d %H:%M:%S.")

        self._params.update({
            'updated_at': DATE_STR
        })

        return self
    
    def varietyof(self, VARIETYOF):
        '''
        Sets the variety of the geomaterial query.

        Args:
            VARIETYOF (int): The variety of the geomaterial.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.varietyof(456)
            >>> gr.save()

        '''
        self._params.update({
            'varietyof': VARIETYOF
        })

        return self

    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
        Executes the query to retrieve the list of geomaterials and saves the results to a specified directory.

        Args:
            OUTDIR (str): The directory path where the retrieved geomaterials will be saved. If not provided, the current directory will be used.
            FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

        Returns:
            None

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.density_min(3.25).saveto("/path/to/directory")

        '''
       
        params = self._params
        end_point = 'geomaterials'
        outdir = OUTDIR
        file_name = FILE_NAME

        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name)

        # reset the query parameters in case the user wants to make another query
        self._init_params()

    def save(self, FILE_NAME = ''):
        '''
        Executes the query to retrieve the list of geomaterials and saves the results to the current directory.

        Args:
            FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

        Returns:
            None

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.density_min(3.25).save()

        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        

    def get_dict(self):
        '''
        Executes the query to retrieve the list of geomaterials and returns the json object.

        Returns:
            list of dictionaries.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> geoObject = gr.density_min(3.25).get_dict()

        '''
       
        params = self._params
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
        
        self._init_params()
        return results


class GeomaterialIdRetriever:
    """
    This module provides the GeomaterialIdRetriever class for returning geomaterial by id
    For more information visit: https://api.mindat.org/schema/redoc/#tag/geomaterials/operation/geomaterials_retrieve

    Usage:
        >>> gir = GeomaterialIdRetriever()
        >>> gir.id(5).save

    Attributes:
        id (int): An int to store id parameter.
    """
    
    def __init__(self):
        self.end_point = "geomaterials"
        self.sub_endpoint = ''
        
        self._params = {}
        self._init_params()

    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}
        self.end_point = "geomaterials"
        self.sub_endpoint = ''
        self.page_size(1500)
        
    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The GeomaterialRetriever object.

        Example:
            >>> gr = GeomaterialRetriever()
            >>> gr.page_size(50)
            >>> gr.save()

        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self

    def id(self, ID, VARIETIES = None):
        '''
        Returns locality with matching id

        Args:
            id (INT): The locality id.
            variety: optional toggle returning varieties with 'y', leave empty if varieties aren't wanted

        Returns:
            self: The GeomaterialIdRetriever() object.

        Example:
            >>> gir = GeomaterialIdRetriever()
            >>> gir.id(2)
            >>> gir.save()
        '''
        
        try:
            ID = int(ID)
        except ValueError:
            raise ValueError("Invalid input. ID must be a valid integer.")
        
        id = str(ID)
        varieties = VARIETIES
        
        if varieties == 'y':
            self.sub_endpoint = '/'.join([id, 'varieties'])
        elif varieties != None:
            raise ValueError(f"Invalid input for 'varieties': {varieties}")
        else:
            self.sub_endpoint = id
        
        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the Geomaterials with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved Geomaterials will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> gir = GeomaterialIdRetriever()
                >>> gir.id(5).saveto("/path/to/directory", "geo5")
        '''

        params = self._params
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        outdir = OUTDIR
        file_name = FILE_NAME

        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name)

        # reset the query parameters in case the user wants to make another query
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of geomaterials and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name
            
            Returns:
                None

            Example:
                >>> gir = GeomaterialIdRetriever()
                >>> gir.id(5).save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve geomaterial with a corresponding id and returns a dictionary.

        Returns:
            List of Dictionaries.

        Example:
            >>> gir = GeomaterialIdRetriever()
            >>> geo5 = gir.id(5).get_dict()

        '''
       
        params = self._params
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
        
        self._init_params()
        return results
        
        
        
        #NOT YET WORKING, check in to see if it returns list vs item
class GeomaterialDictRetriever:
    """
    This module provides the GeomaterialDictRetriever class for returning geomaterial Dictionaries
    For more information visit: https://api.mindat.org/schema/redoc/#tag/geomaterials/operation/geomaterials_dict_retrieve

    Usage:
        >>> gdr = GeomaterialDictRetriever()
        >>> gdr.id(5)

    Attributes:
        id (int): An int to store id parameter.
    """ 
    
    def __init__(self):
        self.end_point = 'geomaterials/dict'
        self.sub_endpoint = ''
        
        self._params = {}
        self._init_params()

    def _init_params(self):
        self.end_point = 'geomaterials/dict'
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
            self: The GeomaterialDictRetriever object.

        Example:
            >>> gdr = GeomaterialDictRetriever()
            >>> gdr.page_size(50)
            >>> gdr.save()

        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the Geomaterials with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved Geomaterials will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> gdr = GeomaterialDictRetriever()
                >>> gdr.saveto("/path/to/directory", "geoDict")
        '''

        params = self._params
        end_point = self.end_point
        outdir = OUTDIR
        file_name = FILE_NAME

        ma = mindat_api.MindatApi()
        ma.download_mindat_json(params, end_point, outdir, file_name)

        # reset the query parameters in case the user wants to make another query
        self._init_params()
    
    def save(self, FILE_NAME = ''):
        '''
            Executes the query to retrieve the list of geomaterials and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name
            
            Returns:
                None

            Example:
                >>> gdr = GeomaterialDictRetriever()
                >>> gdr.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)   
        
    def get_dict(self):
        '''
        Executes the query to retrieve the dictionary of geomaterials.

        Returns:
            dictionary.

        Example:
            >>> gdr = GeomaterialDictRetriever()
            >>> geoDict = gdr.get_dict()

        '''
       
        params = self._params
        end_point = self.end_point

        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
        
        self._init_params()
        return results
        

if __name__ == '__main__':
    gr = GeomaterialRetriever()
    # gr.cleavagetype('Distinct/Good').colour('blue').crystal_system(["Amorphous", "Hexagonal"]).save()
    gr.id__in("3337, 114").save()