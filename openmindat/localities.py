from datetime import datetime

from . import (
    mindat_api,  # noqa: F401  (kept: code patches <module>.mindat_api.MindatApi)
)
from ._base import _R, _as_int, _IdRetriever, _PagedRetriever


class LocalitiesRetriever(_PagedRetriever):
    """
    This module provides the LocalitiesRetriever class for querying locality data from the Mindat API. The class enables users to construct queries based on various parameters such as country, description, included/excluded elements, and more. It supports method chaining for the flexible combination of query parameters and offers functionality to save the queried data either to a specified directory or the current directory.
    For more information visit: https://api.mindat.org/schema/redoc/#tag/localities

    Usage:
        >>> lr = LocalitiesRetriever()
        >>> lr.country("France").description("quartz").saveto("/path/to/directory")

    Attributes:
        _params (dict): A dictionary to store query parameters.

    Methods:
        country(COUNTRY_STR): Sets the country or region for the query.
        description(DESCRIPTION_STR): Sets the description for the query.
        elements_exc(ELEMENTS_EXC): Excludes certain chemical elements from the query.
        elements_inc(ELEMENTS_INC): Includes certain chemical elements in the query.
        expand(EXPAND_FIELDS): Expands the query to include additional fields.
        fields(FIELDS): Specifies the fields to be retrieved in the query.
        id_in(ID_IN_STR): Sets specific IDs for the query.
        omit(OMIT_FIELDS): Omits certain fields from the query results.
        page_size(PAGE_SIZE): Sets the number of results per page.
        txt(TXT_STR): Sets a locality name filter for the query.
        updated_at(DATE_STR): Sets the last updated datetime for the query.
        saveto(OUTDIR): Executes the query and saves the results to the specified directory.
        save(): Executes the query and saves the results to the current directory.

    Press q to quit.
    """

    BASE_ENDPOINT = "v1/localities"

    # Deprecated country method kept for backward compatibility
    def _country(self: _R, COUNTRY_STR: str | None) -> _R:
        """
        Sets the country or region for the query.
        For the list of available countries/regions, please check the API documentation:
        https://api.mindat.org/schema/redoc/#tag/localities/operation/localities_list

        Args:
            COUNTRY_STR (str): The country/region name.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.country("USA")
            >>> lr.saveto()
        """
        valid_options = [
            "162173 Ryugu",
            "Abkhazia",
            "Aegean Sea Plate",
            "Afghanistan",
            "Africa",
            "African Plate",
            "Akrotiri and Dhekelia",
            "Albania",
            "Algeria",
            "Altiplano Plate",
            "Amur Plate",
            "Anatolia Plate",
            "Andorra",
            "Angola",
            "Anguilla",
            "Antarctic Meteorites",
            "Antarctic Plate",
            "Antarctica",
            "Antigua and Barbuda",
            "Arabian Peninsula",
            "Arabian Plate",
            "Arctic Ocean",
            "Argentina",
            "Argentina/Chile",
            "Armenia",
            "Asia",
            "Asia/Europe",
            "Atlantic Ocean",
            "Australia",
            "Australian Plate",
            "Austria",
            "Azerbaijan",
            "Bahamas",
            "Bailiwick of Guernsey",
            "Balmoral Reef Plate",
            "Baltic Sea",
            "Baltic Shield (Fennoscandian Shield)",
            "Banda Sea Plate",
            "Bangladesh",
            "Barbados",
            "Belarus",
            "Belgium",
            "Belize",
            "Belize/Guatemala",
            "Benin",
            "Bermuda",
            "Bhutan",
            "Birds Head Plate",
            "Bolivia",
            "Borneo",
            "Bosnia and Herzegovina",
            "Botswana",
            "Brazil",
            "British Virgin Islands",
            "British and Irish Isles",
            "Brunei",
            "Bulgaria",
            "Burkina Faso",
            "Burma Plate",
            "Burundi",
            "Cambodia",
            "Cameroon",
            "Canada",
            "Cape Verde",
            "Caribbean Plate",
            "Caroline Plate",
            "Cayman Islands",
            "Central Africa",
            "Central African Republic",
            "Central America",
            "Central Asia",
            "Ceres",
            "Chad",
            "Channel Islands",
            "Charon",
            "Chile",
            "China",
            "Cocos Plate",
            "Colombia",
            "Comoro Islands",
            "Comoros",
            "Conway Reef Plate",
            "Cook Islands",
            "Costa Rica",
            "Croatia",
            "Cuba",
            "Cyprus",
            "Czech Republic",
            "Czech Republic/Germany/Poland",
            "Czech Republic/Poland",
            "Czechoslovakia",
            "DR Congo",
            "Denmark",
            "Djibouti",
            "Dominica",
            "Dominican Republic",
            "Earth",
            "East Timor",
            "Easter Plate",
            "Ecuador",
            "Egypt",
            "El Salvador",
            "Equatorial Guinea",
            "Eritrea",
            "Estonia",
            "Eswatini",
            "Ethiopia",
            "Eurasian Plate",
            "Europa",
            "Europe",
            "Falkland Islands",
            "Faroe Islands",
            "Federated States of Micronesia",
            "Fiji",
            "Finland",
            "Finland/Russia",
            "France",
            "French Polynesia",
            "French Southern and Antarctic Lands",
            "Futuna Plate",
            "Gabon",
            "Galapagos Plate",
            "Gambia",
            "Georgia",
            "Germany",
            "Germany/Belgium",
            "Germany/Czech Republic",
            "Germany/Poland",
            "Ghana",
            "Gibraltar",
            "Greece",
            "Greenland",
            "Grenada",
            "Guatemala",
            "Guinea",
            "Guinea-Bissau",
            "Guyana",
            "Haiti",
            "Hans Island",
            "Honduras",
            "Hungary",
            "Iberian Peninsula",
            "Iceland",
            "Ilemi Triangle",
            "India",
            "Indian Ocean",
            "Indian Plate (India Plate)",
            "Indonesia",
            "Io",
            "Iran",
            "Iraq",
            "Ireland",
            "Ireland (island)",
            "Island of Cyprus",
            "Isle of Man",
            "Israel",
            "Italy",
            "Ivory Coast",
            "Jamaica",
            "Japan",
            "Jersey",
            "Jordan",
            "Juan Fernandez Plate",
            "Juan de Fuca Plate",
            "Kazakhstan",
            "Kazakhstan/Russia",
            "Kenya",
            "Kiribati",
            "Korea",
            "Korean Peninsula",
            "Kosovo",
            "Kuwait",
            "Kyrgyzstan",
            "Laos",
            "Latvia",
            "Lebanon",
            "Lesotho",
            "Liberia",
            "Libya",
            "Liechtenstein",
            "Lithuania",
            "Luxembourg",
            "Madagascar",
            "Malawi",
            "Malawi/Mozambique/Tanzania",
            "Malaysia",
            "Maldives",
            "Mali",
            "Malta",
            "Manus Plate",
            "Maoke Plate",
            "Mariana Plate",
            "Mars",
            "Marshall Islands",
            "Mauritania",
            "Mauritius",
            "Mercury",
            "Mexico",
            "Middle East",
            "Mimas",
            "Moldova",
            "Molucca Sea Plate",
            "Monaco",
            "Mongolia",
            "Montenegro",
            "Montserrat",
            "Morocco",
            "Mozambique",
            "Myanmar",
            "Namibia",
            "Nauru",
            "Nazca Plate",
            "Nepal",
            "Netherlands",
            "Netherlands Antilles",
            "New Guinea",
            "New Hebrides Plate",
            "New Zealand",
            "Nicaragua",
            "Niger",
            "Nigeria",
            "Niuafo'ou Plate",
            "Niue",
            "North Africa",
            "North America",
            "North America Plate",
            "North Andes plate",
            "North Atlantic Igneous Province",
            "North Bismarck Plate",
            "North Korea",
            "North Macedonia",
            "North Sea",
            "Northern Cyprus",
            "Northern Mariana Islands",
            "Northwest Africa",
            "Northwest Africa Meteorites",
            "Norway",
            "Okhotsk Plate",
            "Okinawa Plate",
            "Oman",
            "Outer Space",
            "Pacific Ocean",
            "Pacific Plate",
            "Pakistan",
            "Palau",
            "Palestine",
            "Panama",
            "Panama Plate",
            "Papua New Guinea",
            "Paraguay",
            "Persian Gulf",
            "Peru",
            "Philippine Sea Plate",
            "Philippines",
            "Phobos",
            "Pitcairn Islands",
            "Pluto",
            "Poland",
            "Portugal",
            "Puerto Rico",
            "Qatar",
            "Red Sea",
            "Republic of the Congo",
            "Rivera Plate",
            "Romania",
            "Russia",
            "Rwanda",
            "Réunion Island",
            "Saint Helena",
            "Saint Helena, Ascension and Tristan da Cunha",
            "Saint Kitts and Nevis",
            "Saint Lucia",
            "Saint Martin",
            "Saint Vincent and the Grenadines",
            "Samoa",
            "Samoan Islands",
            "San Marino",
            "Sandwich Plate",
            "Saudi Arabia",
            "Scandinavia",
            "Scotia Plate",
            "Senegal",
            "Serbia",
            "Serbia and Montenegro",
            "Seychelles",
            "Shetland Plate",
            "Sierra Leone",
            "Singapore",
            "Slovakia",
            "Slovenia",
            "Solomon Islands",
            "Solomon Sea Plate",
            "Somali Plate",
            "Somalia",
            "Somaliland",
            "South Africa",
            "South America",
            "South America Plate",
            "South Bismarck Plate",
            "South China Sea",
            "South Georgia and the South Sandwich Islands",
            "South Kordofan Sudan",
            "South Korea",
            "South Ossetia",
            "South Sudan",
            "Southern Africa",
            "Soviet Union (1922-1991)",
            "Spain",
            "Sri Lanka",
            "Sudan",
            "Sunda Plate",
            "Suriname",
            "Swaziland",
            "Sweden",
            "Switzerland",
            "Syria",
            "São Tomé and Príncipe",
            "Taiwan",
            "Tajikistan",
            "Tanzania",
            "Thailand",
            "The Caribbean",
            "The Moon",
            "Timor Plate",
            "Togo",
            "Tonga",
            "Tonga Plate",
            "Trinidad and Tobago",
            "Triton",
            "Tunisia",
            "Turkestan",
            "Turkey",
            "Turkmenistan",
            "Turks and Caicos Islands",
            "Tuvalu",
            "U.S. Virgin Islands",
            "UK",
            "USA",
            "Uganda",
            "Ukraine",
            "United Arab Emirates",
            "United States Minor Outlying Islands",
            "Uruguay",
            "Uzbekistan",
            "Vanuatu",
            "Venezuela",
            "Venus",
            "Vermont",
            "Vietnam",
            "West Africa",
            "Western Sahara",
            "Woodlark Plate",
            "Yangtze Plate",
            "Yellow Sea",
            "Yemen",
            "Zambia",
            "Zimbabwe",
        ]

        if COUNTRY_STR is not None:
            if isinstance(COUNTRY_STR, str):
                country = COUNTRY_STR
            else:
                raise TypeError("Country must be a string")

            if country not in valid_options:
                print(
                    f"Potentioally invalid input: {country}.\nPlease refer to https://api.mindat.org/schema/redoc/#tag/localities/operation/localities_list"
                )

            self._params.update({"country": country})

        return self

    def country(self: _R, COUNTRY_STR: str | None) -> _R:
        """
        Sets the country or region for the query.

        Args:
            COUNTRY_STR (str): The country/region name.

        Returns:
            self: The LocalitiesRetriever object.
        """
        # MODIFICATION: Removed the massive hardcoded 'valid_options' list.
        # It is better to allow any string to prevent the library from breaking
        # when Mindat updates their country list or spelling.

        if COUNTRY_STR is not None:
            if isinstance(COUNTRY_STR, str):
                self._params.update({"country": COUNTRY_STR})
            else:
                raise TypeError("Country must be a string")

        return self

    def description(self: _R, DESCRIPTION_STR: str) -> _R:
        """
        Sets the description for the query.

        Args:
            DESCRIPTION_STR (str): The description.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.description("quartz")
            >>> lr.saveto()
        """
        self._params.update({"description": DESCRIPTION_STR})

        return self

    def elements_exc(self: _R, ELEMENTS_EXC: str) -> _R:
        """
        Exclude chemical elements.

        Args:
            ELEMENTS_EXC (str): Comma-separated string of chemical elements to exclude.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.elements_exc("Au,Ag")
            >>> lr.save()

        """

        elements_exc = ELEMENTS_EXC
        self._params.update({"elements_exc": elements_exc})

        return self

    def elements_inc(self: _R, ELEMENTS_INC: str) -> _R:
        """
        Include chemical elements.

        Args:
            ELEMENTS_INC (str): Comma-separated string of chemical elements to include.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.elements_inc("Fe,Cu")
            >>> lr.save()

        """

        elements_inc = ELEMENTS_INC
        self._params.update({"elements_inc": elements_inc})

        return self

    def expand(self: _R, EXPAND_FIELDS: str | list[str]) -> _R:
        """
        Expand the query to include related minerals and select specific fields to expand.

        Args:
            EXPAND_FIELDS(list[str] or str): The fields to expand. Valid options are:
                - "geomaterials"
                - "~all"
                - "*"

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.expand(["description", "type_localities"])
            >>> lr.saveto()
        """

        valid_options = ["geomaterials", "~all", "*"]

        if isinstance(EXPAND_FIELDS, str):
            EXPAND_FIELDS = [EXPAND_FIELDS]

        # Taken after the str -> list step: before 0.1.4 a string was split into letters.
        expand_fields = EXPAND_FIELDS

        invalid_options = [
            field for field in EXPAND_FIELDS if field not in valid_options
        ]

        if invalid_options:
            print(
                f"Possible Invalid EXPAND_FIELDS: {', '.join(invalid_options)}\nYou can find valid options at https://api.mindat.org/schema/redoc/#tag/localities"
            )

            # Changes * to "*" and from a list to a string since this is what the param will read without failing.
        expand_fields = [w.replace("*", '"*"') for w in expand_fields]
        expand_fields_string = ",".join(expand_fields)

        self._params.update({"expand": expand_fields_string})

        return self

    def fields(self: _R, FIELDS: str) -> _R:
        """
        Specify the selected fields to be retrieved for each geomaterial.
        Please check the API documentation for the list of available fields.
        https://api.mindat.org/schema/redoc/#tag/minerals_ima/operation/minerals_ima_list

        Args:
            FIELDS (str): The selected fields to be retrieved. Multiple fields should be separated by commas.

        Example Input:
            fields=fields=id,longid,guid,txt,revtxtd,description_short,latitude,longitude,langtxt,dateadd,datemodify,elements,country,refs,coordsystem,parent,links,area,non_hierarchical,age,meteorite_type,company,company2,loc_status,loc_group,status_year,company_year,discovered_before,discovery_year,discovery_year_type,level,locsinclude,locsexclude,wikipedia,osmid,geonames,timestamp,~all,*
        Returns:
            self: The LocalitiesRetriever object.
        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.fields("id,name,ima_formula")
            >>> lr.saveto()
        """

        self._params.update({"fields": FIELDS})

        return self

    def id_in(self: _R, ID_IN_STR: str) -> _R:
        """
        Set the IDs for the query.

        Args:
            ID_IN_STR (str): The IDs to filter the query, separated by commas.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.id_in("123,456,789")
            >>> lr.saveto()
        """

        ids = str(ID_IN_STR)

        self._params.update({"id_in": ids})

        return self

    def omit(self: _R, OMIT_FIELDS: str) -> _R:
        """
        Set the fields to omit from the query.

        Args:
            OMIT_FIELDS (str): The fields to omit, separated by commas.
            Please check the API documentation for the list of available fields.
            https://api.mindat.org/schema/redoc/#tag/localities

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.omit("id,longid")
            >>> lr.saveto()
        """

        omit_fields = OMIT_FIELDS
        self._params.update({"omit": omit_fields})

        return self

    def page(self: _R, PAGE: int) -> _R:
        """
        Sets the page number within the paginated result set.

        Args:
            PAGE (int): The page number.

        Returns:
            self: The LocalitiesRetriever object.
        """
        try:
            val = int(PAGE)
        except ValueError:
            raise ValueError("Page must be an integer.")

        self._params.update({"page": val})

        return self

    def txt(self: _R, TXT_STR: str) -> _R:
        """
        Sets the locality name filter.

        Args:
            TXT_STR (str): The locality name to filter by.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.txt("example locality")
            >>> lr.saveto()
        """
        self._params.update({"txt": TXT_STR})

        return self

    def updated_at(self: _R, DATE_STR: str) -> _R:
        """
        Sets the last updated datetime for the geomaterial query.

        Args:
            DATE_STR (str): The last updated datetime in the format %Y-%m-%d %H:%M:%S.

        Returns:
            self: The LocalitiesRetriever object.

        Raises:
            ValueError: If the provided DATE_STR is not a valid datetime string.

        Example:
            >>> retriever = LocalitiesRetriever()
            >>> retriever.updated_at('2022-01-01 12:00:00')
            >>> retriever.save()
        """
        try:
            datetime.strptime(DATE_STR, "%Y-%m-%d %H:%M:%S")  # noqa: DTZ007  (format check only)
        except ValueError:
            raise ValueError(
                "Invalid datetime format. Please provide the datetime in the format %Y-%m-%d %H:%M:%S."
            )

        self._params.update({"updated_at": DATE_STR})

        return self

    def level_gte(self: _R, LEVEL: int) -> _R:
        '''
        Returns localities whose hierarchy level is >= LEVEL (0 = country).

        Args:
            LEVEL (int): The value.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.country("Norway").level_gte(3).get_dict()
        '''
        self._params.update({"level_gte": _as_int(LEVEL, "LEVEL")})
        return self

    def level_lte(self: _R, LEVEL: int) -> _R:
        '''
        Returns localities whose hierarchy level is <= LEVEL (0 = country).

        Args:
            LEVEL (int): The value.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.country("Norway").level_lte(1).get_dict()
        '''
        self._params.update({"level_lte": _as_int(LEVEL, "LEVEL")})
        return self

    def sublocs_gte(self: _R, COUNT: int) -> _R:
        '''
        Returns localities with at least COUNT sub-localities.

        Args:
            COUNT (int): The value.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.country("Norway").sublocs_gte(10).get_dict()
        '''
        self._params.update({"sublocs_gte": _as_int(COUNT, "COUNT")})
        return self

    def sublocs_lte(self: _R, COUNT: int) -> _R:
        '''
        Returns localities with at most COUNT sub-localities.

        Args:
            COUNT (int): The value.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.country("Norway").sublocs_lte(0).get_dict()
        '''
        self._params.update({"sublocs_lte": _as_int(COUNT, "COUNT")})
        return self

    def non_hierarchial(self: _R, IS_NON_HIERARCHICAL: bool) -> _R:
        '''
        Filters on the non-hierarchical locality flag. The spelling follows the Mindat API
        parameter; non_hierarchical() is an alias.

        Args:
            IS_NON_HIERARCHICAL (bool): True for non-hierarchical localities only.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.country("Norway").non_hierarchial(True).get_dict()
        '''
        self._params.update({"non_hierarchial": bool(IS_NON_HIERARCHICAL)})
        return self

    def non_hierarchical(self, IS_NON_HIERARCHICAL: bool) -> "LocalitiesRetriever":
        '''
        Alias of non_hierarchial() with the usual spelling.
        '''
        return self.non_hierarchial(IS_NON_HIERARCHICAL)

    def revtxtd_istartswith(self: _R, PREFIX: str) -> _R:
        '''
        Returns localities whose reversed full name starts with PREFIX (case-insensitive).
        The reversed name lists the country first, e.g. "Norway, Agder, Åmli".

        Args:
            PREFIX (str): The start of the reversed locality name.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.revtxtd_istartswith("Norway, Agder").get_dict()
        '''
        self._params.update({"revtxtd_istartswith": PREFIX})
        return self


class LocalitiesIdRetriever(_IdRetriever):
    """
    This module provides the LocalitiesIdRetriever class for returning localities by id
    For more information visit: https://api.mindat.org/schema/redoc/#tag/localities/operation/localities_retrieve

    Usage:
        >>> lir = LocalitiesIdRetriever()
        >>> lir.id(5)

    Attributes:
        id (int): An int to store id parameter.
    """

    BASE_ENDPOINT = "v1/localities"

    # Same check as LocalitiesRetriever.country(): on a single locality the Mindat API
    # returns 404 when the locality is not in that country.
    country = LocalitiesRetriever.country


if __name__ == "__main__":
    lr = LocalitiesRetriever()
    lr.country("UK").save()
