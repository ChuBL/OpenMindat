from . import mindat_api
from datetime import datetime

class LocalitiesRetriever:
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
        cursor(CURSOR_STR): Sets the pagination cursor for the query.
        description(DESCRIPTION_STR): Sets the description for the query.
        elements_exc(ELEMENTS_EXC): Excludes certain chemical elements from the query.
        elements_inc(ELEMENTS_INC): Includes certain chemical elements in the query.
        expand(EXPAND_FIELDS): Expands the query to include additional fields.
        fields(FIELDS): Specifies the fields to be retrieved in the query.
        id__in(ID_IN_STR): Sets specific IDs for the query.
        omit(OMIT_FIELDS): Omits certain fields from the query results.
        page_size(PAGE_SIZE): Sets the number of results per page.
        txt(TXT_STR): Sets a locality name filter for the query.
        updated_at(DATE_STR): Sets the last updated datetime for the query.
        saveto(OUTDIR): Executes the query and saves the results to the specified directory.
        save(): Executes the query and saves the results to the current directory.

    Press q to quit.
    """

    def __init__(self):
        self._params = {}
        self.end_point = 'localities'
        self._init_params()

    def _init_params(self):
        self.end_point = 'localities'
        self._params.clear()
        self._params = {'format': 'json'}
        self.page_size(1500)

    def country(self, COUNTRY_STR):
        '''
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
        '''
        valid_options = ["162173 Ryugu","Abkhazia","Aegean Sea Plate","Afghanistan","Africa","African Plate","Akrotiri and Dhekelia","Albania","Algeria","Altiplano Plate","Amur Plate","Anatolia Plate","Andorra","Angola","Anguilla","Antarctic Meteorites","Antarctic Plate","Antarctica","Antigua and Barbuda","Arabian Peninsula","Arabian Plate","Arctic Ocean","Argentina","Argentina/Chile","Armenia","Asia","Asia/Europe","Atlantic Ocean","Australia","Australian Plate","Austria","Azerbaijan","Bahamas","Bailiwick of Guernsey","Balmoral Reef Plate","Baltic Sea","Baltic Shield (Fennoscandian Shield)","Banda Sea Plate","Bangladesh","Barbados","Belarus","Belgium","Belize","Belize/Guatemala","Benin","Bermuda","Bhutan","Birds Head Plate","Bolivia","Borneo","Bosnia and Herzegovina","Botswana","Brazil","British Virgin Islands","British and Irish Isles","Brunei","Bulgaria","Burkina Faso","Burma Plate","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Caribbean Plate","Caroline Plate","Cayman Islands","Central Africa","Central African Republic","Central America","Central Asia","Ceres","Chad","Channel Islands","Charon","Chile","China","Cocos Plate","Colombia","Comoro Islands","Comoros","Conway Reef Plate","Cook Islands","Costa Rica","Croatia","Cuba","Cyprus","Czech Republic","Czech Republic/Germany/Poland","Czech Republic/Poland","Czechoslovakia","DR Congo","Denmark","Djibouti","Dominica","Dominican Republic","Earth","East Timor","Easter Plate","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia","Eurasian Plate","Europa","Europe","Falkland Islands","Faroe Islands","Federated States of Micronesia","Fiji","Finland","Finland/Russia","France","French Polynesia","French Southern and Antarctic Lands","Futuna Plate","Gabon","Galapagos Plate","Gambia","Georgia","Germany","Germany/Belgium","Germany/Czech Republic","Germany/Poland","Ghana","Gibraltar","Greece","Greenland","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Hans Island","Honduras","Hungary","Iberian Peninsula","Iceland","Ilemi Triangle","India","Indian Ocean","Indian Plate (India Plate)","Indonesia","Io","Iran","Iraq","Ireland","Ireland (island)","Island of Cyprus","Isle of Man","Israel","Italy","Ivory Coast","Jamaica","Japan","Jersey","Jordan","Juan Fernandez Plate","Juan de Fuca Plate","Kazakhstan","Kazakhstan/Russia","Kenya","Kiribati","Korea","Korean Peninsula","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Madagascar","Malawi","Malawi/Mozambique/Tanzania","Malaysia","Maldives","Mali","Malta","Manus Plate","Maoke Plate","Mariana Plate","Mars","Marshall Islands","Mauritania","Mauritius","Mercury","Mexico","Middle East","Mimas","Moldova","Molucca Sea Plate","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nazca Plate","Nepal","Netherlands","Netherlands Antilles","New Guinea","New Hebrides Plate","New Zealand","Nicaragua","Niger","Nigeria","Niuafo'ou Plate","Niue","North Africa","North America","North America Plate","North Andes plate","North Atlantic Igneous Province","North Bismarck Plate","North Korea","North Macedonia","North Sea","Northern Cyprus","Northern Mariana Islands","Northwest Africa","Northwest Africa Meteorites","Norway","Okhotsk Plate","Okinawa Plate","Oman","Outer Space","Pacific Ocean","Pacific Plate","Pakistan","Palau","Palestine","Panama","Panama Plate","Papua New Guinea","Paraguay","Persian Gulf","Peru","Philippine Sea Plate","Philippines","Phobos","Pitcairn Islands","Pluto","Poland","Portugal","Puerto Rico","Qatar","Red Sea","Republic of the Congo","Rivera Plate","Romania","Russia","Rwanda","Réunion Island","Saint Helena","Saint Helena， Ascension and Tristan da Cunha","Saint Kitts and Nevis","Saint Lucia","Saint Martin","Saint Vincent and the Grenadines","Samoa","Samoan Islands","San Marino","Sandwich Plate","Saudi Arabia","Scandinavia","Scotia Plate","Senegal","Serbia","Serbia and Montenegro","Seychelles","Shetland Plate","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Solomon Sea Plate","Somali Plate","Somalia","Somaliland","South Africa","South America","South America Plate","South Bismarck Plate","South China Sea","South Georgia and the South Sandwich Islands","South Kordofan Sudan","South Korea","South Ossetia","South Sudan","Southern Africa","Soviet Union (1922-1991)","Spain","Sri Lanka","Sudan","Sunda Plate","Suriname","Swaziland","Sweden","Switzerland","Syria","São Tomé and Príncipe","Taiwan","Tajikistan","Tanzania","Thailand","The Caribbean","The Moon","Timor Plate","Togo","Tonga","Tonga Plate","Trinidad and Tobago","Triton","Tunisia","Turkestan","Turkey","Turkmenistan","Turks and Caicos Islands","Tuvalu","U.S. Virgin Islands","UK","USA","Uganda","Ukraine","United Arab Emirates","United States Minor Outlying Islands","Uruguay","Uzbekistan","Vanuatu","Venezuela","Venus","Vermont","Vietnam","West Africa","Western Sahara","Woodlark Plate","Yangtze Plate","Yellow Sea","Yemen","Zambia","Zimbabwe"]
        
        if COUNTRY_STR is not None:
            if isinstance(COUNTRY_STR, str):
                country = COUNTRY_STR  
            else:
                raise TypeError("Country must be a string")

            if country not in valid_options:
                print(f"Potentioally invalid input: {country}.\nPlease refer to https://api.mindat.org/schema/redoc/#tag/localities/operation/localities_list")

            self._params.update({
                'country': country
            })  

        return self
    
    def cursor(self, CURSOR_STR):
        '''
        Sets the pagination cursor value for the query.

        Args:
            CURSOR_STR (str): The pagination cursor value.

        Returns:
            self: The LocalitiesRetriever object.
        '''
        self._params.update({
            'cursor': CURSOR_STR
        })

        return self

    def description(self, DESCRIPTION_STR):
        '''
        Sets the description for the query.

        Args:
            DESCRIPTION_STR (str): The description.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.description("quartz")
            >>> lr.saveto()
        '''
        self._params.update({
            'description': DESCRIPTION_STR
        })

        return self
    
    def elements_exc(self, ELEMENTS_EXC):
        '''
        Exclude chemical elements.

        Args:
            ELEMENTS_EXC (str): Comma-separated string of chemical elements to exclude.

        Returns:
            self: The LocalitiesRetriever object.
        
        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.elements_exc("Au,Ag")
            >>> lr.save()

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
            self: The LocalitiesRetriever object.
        
        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.elements_inc("Fe,Cu")
            >>> lr.save()

        '''

        elements_inc = ELEMENTS_INC
        self._params.update({
            'elements_inc': elements_inc
        })

        return self

    def expand(self, EXPAND_FIELDS):
        '''
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
        '''

        valid_options = ["geomaterials", "~all", "*"]

        if isinstance(EXPAND_FIELDS, str):
            EXPAND_FIELDS = [EXPAND_FIELDS]

        invalid_options = [field for field in EXPAND_FIELDS if field not in valid_options]

        if invalid_options:
            raise ValueError(f"Invalid EXPAND_FIELDS: {', '.join(invalid_options)}\nEXPAND_FIELDS must be one or more of the following: {', '.join(valid_options)}")

        expand_fields = EXPAND_FIELDS
        self._params.update({
            'expand': expand_fields
        })

        return self
    
    def fields(self, FIELDS):
        '''
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
        '''

        self._params.update({
            'fields': FIELDS
        })

        return self
    
    def id__in(self, ID_IN_STR):
        '''
        Set the IDs for the query.

        Args:
            ID_IN_STR (str): The IDs to filter the query, separated by commas.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.id__in("123,456,789")
            >>> lr.saveto()
        '''

        ids = str(ID_IN_STR)

        self._params.update({
            'id__in': ids
        })

        return self

    
    def omit(self, OMIT_FIELDS):
        '''
        Set the fields to omit from the query.

        Args:
            OMIT_FIELDS (str): The fields to omit, separated by commas. 
            Please check the API documentation for the list of available fields.
            https://api.mindat.org/schema/redoc/#tag/minerals_ima/operation/minerals_ima_list
        
        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.omit("id,longid")
            >>> lr.saveto()
        '''

        omit_fields = OMIT_FIELDS
        self._params.update({
            'omit': omit_fields
        })

        return self
    

    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The LocalitiesRetriever object.
            
        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.page_size(50)
            >>> lr.saveto()
        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def txt(self, TXT_STR):
        '''
        Sets the locality name filter.

        Args:
            TXT_STR (str): The locality name to filter by.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.txt("example locality")
            >>> lr.saveto()
        '''
        self._params.update({
            'txt': TXT_STR
        })

        return self
    
    def updated_at(self, DATE_STR):
        '''	
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
        '''
        try:
            datetime.strptime(DATE_STR, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid datetime format. Please provide the datetime in the format %Y-%m-%d %H:%M:%S.")

        self._params.update({
            'updated_at': DATE_STR
        })

        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the localities with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved localities will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> lr = LocalitiesRetriever()
                >>> lr.saveto("/path/to/directory", "france")
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
            Executes the query to retrieve the list of localities and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name
            
            Returns:
                None

            Example:
                >>> lr = LocalitiesRetriever()
                >>> lr.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve the list of localities and returns the json object.

        Returns:
            list of dictionaries.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> france = lr.country('France').get_dict()

        '''
       
        params = self._params
        end_point = self.end_point
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
        
        self._init_params()
        return results
        
        
class LocalitiesIdRetriever:
    """
    This module provides the LocalitiesIdRetriever class for returning localities by id
    For more information visit: https://api.mindat.org/schema/redoc/#tag/localities/operation/localities_retrieve

    Usage:
        >>> lir = LocalitiesIdRetriever()
        >>> lir.id(5)

    Attributes:
        id (int): An int to store id parameter.
    """
    
    def __init__(self):
        self.end_point = 'localities'
        self.sub_endpoint = ''
        
        self._params = {}
        self._init_params()

    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}
        self.end_point = 'localities'
        self.sub_endpoint = ''
        self.page_size(1500)
        
    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The LocalitiesIdRetriever object.
            
        Example:
            >>> lidr = LocalitiesRetriever()
            >>> lidr.page_size(50)
            >>> lidr.saveto()
        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self

    def id(self, ID):
        '''
        Returns locality with matching id

        Args:
            id (INT): The locality id.

        Returns:
            self: The LocalitiesIdRetriever() object.

        Example:
            >>> lir = LocalitiesIdRetriever()
            >>> lir.id(2)
            >>> lir.save()
        '''
        
        try:
            ID = int(ID)
        except ValueError:
            raise ValueError("Invalid input. ID must be a valid integer.")
        
        id = str(ID)
        
        self.sub_endpoint = id
        
        return self
    
    def saveto(self, OUTDIR = '', FILE_NAME = ''):
        '''
            Executes the query to retrieve the localities with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved localities will be saved. If not provided, the current directory will be used.
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name

            Returns:
                None

            Example:
                >>> lir = LocalitiesIdRetriever()
                >>> lir.saveto("/path/to/directory", "france")
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
            Executes the query to retrieve the list of localities and saves the results to the current directory.

            Args:
                FILE_NAME (str): An optional file name, if no input is given it uses the end point as a name
            
            Returns:
                None

            Example:
                >>> lir = LocalitiesIdRetriever()
                >>> lir.save()
        '''
        file_name = FILE_NAME
        
        self.saveto('', file_name)
        
    def get_dict(self):
        '''
        Executes the query to retrieve locality with a corresponding id and returns a dictionary.

        Returns:
            List of Dictionaries.

        Example:
                >>> lir = localitiesIdRetriever()
                >>> locality5 = lir.id(5).get_dict()

        '''
       
        params = self._params
        end_point = '/'.join([self.end_point, self.sub_endpoint])
        
        ma = mindat_api.MindatApi()
        results = ma.get_mindat_json(params, end_point)
        
        self._init_params()
        return results

if __name__ == '__main__':
    lr = LocalitiesRetriever()
    lr.country("UK").save()
