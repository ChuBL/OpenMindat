"""
This module provides a suite of tools for querying mineral and geomaterial data from the Mindat API.
These classes offer flexible query parameters, method chaining, and functionality to save query results to a specified location.

Attributes:
    MineralsIMARetriever (class): A class for querying mineral data based on IMA status and other parameters.
    GeomaterialSearchRetriever (class): A class for searching geomaterials using specific keywords.
    GeomaterialRetriever (class): A class for performing detailed queries on geomaterials.

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
        >>> mir.ima(1).fields("id,name,ima_formula,ima_year")
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
from . import mindat_api
from .minerals_ima import MineralsIMARetriever
from .minerals_ima import MineralsIdRetriever
from .geomaterials_search import GeomaterialSearchRetriever
from .geomaterials import GeomaterialRetriever
from .geomaterials import GeomaterialIdRetriever
from .geomaterials import GeomaterialDictRetriever
from .localities import LocalitiesRetriever
from .localities import LocalitiesIdRetriever
from .countries import CountriesRetriever
from .dana8 import DanaRetriever
from .nickel_strunz import StrunzRetriever

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