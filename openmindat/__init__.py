"""
This module provides a suite of tools for querying mineral and geomaterial data from the Mindat API.
These classes offer flexible query parameters, method chaining, and functionality to save query results to a specified location.

Attributes:
    MineralsIMARetriever (class): A class for querying mineral data based on IMA status and other parameters.
    MineralIdRetriever (class): A class for querying mineral IMA data based on id.
    GeomaterialSearchRetriever (class): A class for searching geomaterials using specific keywords.
    GeomaterialRetriever (class): A class for performing detailed queries on geomaterials.
    GeomaterialIdRetriever (class): A class for querying geomaterials based on id.
    GeomaterialDictRetriever (class): A class for displaying a dictionary of values for a field.
    LocalitiesRetriever (class): A class for performing detailed queries based on localities.
    LocalitiesIdRetriever (class): A class for finding locality data based on id.
    LocalitiesAgeRetriever (class): A class for querying locality age data.
    LocalitiesAgeIdRetriever (class): A class for querying locality age based on id.
    LocalitiesStatusRetriever (class): A class for querying locality status data.
    LocalitiesStatusIdRetriever (class): A class for querying locality status based on id.
    LocalitiesTypeRetriever (class): A class for querying locality type data.
    LocalitiesTypeIdRetriever (class): A class for querying locality type based on id.
    GeoRegionRetriever (class): A class for querying locality georegion data.
    LocObjectRetriever (class): A class for querying locality object data based on id.
    CountriesListRetriever (class): A class for querying country data from OpenMindat.
    CountriesIdRetriever (class): A class for querying country data based on id.
    DanaRetriever (class): A class for querying dana-8 group and subgroup data. 
    StrunzRetriever (class): A class for querying different types of nickel-strunz-10 data.
    PhotoCountRetriever(class): A class to facilitate the retrieval of photo count data from the Mindat API.
    

Todo:
    * Expand the module with additional classes and functions as needed.
    * Implement additional filters and query options for enhanced data retrieval.

Note:
    Ensure that the Mindat API is accessible and properly configured before using these classes.

Examples:
    Using the help function to view the docstring for classes, such as GeomaterialRetriever:
        >>> help(GeomaterialRetriever)

    Using the MineralsIMARetriever class to retrieve IMA-approved minerals:
        >>> mir = MineralsIMARetriever()
        >>> mir.fields("id,name,ima_formula,ima_year")
        >>> mir.saveto("/path/to/minerals_data")

    Searching geomaterials with specific keywords using GeomaterialSearchRetriever:
        >>> gsr = GeomaterialSearchRetriever()
        >>> gsr.geomaterials_search("quartz, green, hexagonal")
        >>> gsr.save()

    Performing a detailed query with GeomaterialRetriever:
        >>> gr = GeomaterialRetriever()
        >>> gr.density_min(2.0).density_max(5.0).crystal_system("Hexagonal")
        >>> gr.elements_exc("Au,Ag")
        >>> gr.saveto("/path/to/geomaterials_data")
        
Press q to quit.
"""
from .mindat_api import MindatApi, MindatApiKeyManeger
from .minerals_ima import MineralsIMARetriever
from .minerals_ima import MineralsIdRetriever
from .geomaterials_search import GeomaterialSearchRetriever
from .geomaterials import GeomaterialRetriever
from .geomaterials import GeomaterialIdRetriever
from .geomaterials import GeomaterialDictRetriever
from .localities import LocalitiesRetriever
from .localities import LocalitiesIdRetriever
from .localities_age import LocalitiesAgeRetriever
from .localities_age import LocalitiesAgeIdRetriever
from .localities_status import LocalitiesStatusRetriever
from .localities_status import LocalitiesStatusIdRetriever
from .localities_type import LocalitiesTypeRetriever
from .localities_type import LocalitiesTypeIdRetriever
from .locgeoregion2 import GeoRegionRetriever
from .locobject import LocobjectRetriever
from .countries import CountriesListRetriever
from .countries import CountriesIdRetriever
from .dana8 import DanaRetriever
from .nickel_strunz import StrunzRetriever
from .photo_count import PhotoCountRetriever

if __name__ == "__main__":
    # --------------------------------------------
    # Use case 1: Search for a geomaterial by name
    
    # Check the docstring for GeomaterialSearchRetriever for more information
    help(MineralsIMARetriever)

    # Create an instance of MineralsIMARetriever
    mir = MineralsIMARetriever()

    # Set query parameters such as IMA status and specific fields
    mir.ima(1)  # Include only IMA-approved names
    mir.fields("id,name,ima_formula,ima_year")

    # Execute the query and save the results to a specific directory
    mir.saveto("/path/to/minerals_data")

    # --------------------------------------------
    # --------------------------------------------

    # Use case 2: Search for a geomaterial by keywords

    # Check the docstring for GeomaterialSearchRetriever for more information
    help(GeomaterialSearchRetriever)

    # Create an instance of GeomaterialSearchRetriever
    gsr = GeomaterialSearchRetriever()

    # Search for geomaterials using specific keywords
    gsr.geomaterials_search("quartz, green, hexagonal")

    # Execute the query and save the results to the current directory
    gsr.save()

    # --------------------------------------------
    # --------------------------------------------

    # Use case 3: Search for a geomaterial by specific parameters
    # Create an instance of GeomaterialRetriever
    gr = GeomaterialRetriever()

    # Set various query parameters like density range and crystal system
    gr.density_min(2.0)
    gr.density_max(5.0)
    gr.crystal_system("Hexagonal")

    # Optionally exclude certain elements
    gr.elements_exc("Au,Ag")

    # Execute the query and save the results to a specified directory
    gr.saveto("/path/to/geomaterials_data")