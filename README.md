> [!Caution]
> Due to the recent changes in the Mindat API, the OpenMindat package is currently undergoing updates. Some functionalities may not work as expected. We are actively working on resolving these issues and appreciate your patience.

# OpenMindat: A Python Package for Geomaterial Data Analysis and Retrieval from Mindat API

The OpenMindat Python package is designed to facilitate querying and retrieving data on minerals and geomaterials from the Mindat API. It provides classes for detailed queries based on various attributes like IMA status, keywords, and specific geomaterial properties.

GitHub Repository: [OpenMindat Python Package](https://github.com/ChuBL/OpenMindat)

## Table of Contents
  - [Get Started](#get-started)
  - [Endpoint Descriptions](#endpoint-descriptions)
  - [Use Cases](#use-cases)
    - [0. Setup](#0-setup)
    - [1. Perform Detailed Queries on Geomaterials](#1-perform-detailed-queries-on-geomaterials)
    - [2. Retrieve IMA-Approved Minerals](#2-retrieve-ima-approved-minerals)
    - [3. Search Geomaterials Using Keywords](#3-search-geomaterials-using-keywords)
    - [4. Retrieve Localities](#4-retrieve-localities)
    - [5. Retrieve Type Localities for IMA-Approved Mineral Species](#5-retrieve-type-localities-for-ima-approved-mineral-species)
    - [6. Retrieve Locality Occurrences for Single Mineral Species](#6-retrieve-locality-occurrences-for-single-mineral-species)
  - [Documentation and Relevant Links](#documentation-and-links)
  - [Contact Us](#contact-us)
  - [License](#license)
  - [Authors](#authors)
  - [Citations](#citations)
  - [Acknowledgments](#acknowledgments)
  - [Change Logs](#change-logs)

## Get Started

### Install via Pip

```console
foo@bar:~$ pip install openmindat
```

### Import the Package in Python

```python
import openmindat
```

<p float="left">
        <img src="https://raw.githubusercontent.com/ChuBL/OpenMindat/main/figures/OpenMindat_Flowchart.png"  width="100%">
</p>

## Endpoint Descriptions 

| Endpoint | Classes | Description |
|:------------------:|------------|----------|
| Dana8              |   - [DanaRetriever()](https://github.com/ChuBL/OpenMindat/wiki/DanaRetriever)   |   Search query to return information about the Dana-8 classification standard.   |
| Geomaterials       |  - [GeomaterialRetriever()](https://github.com/ChuBL/OpenMindat/wiki/GeomaterialRetriever)<br>- [GeomaterialIdRetreiver()](https://github.com/ChuBL/OpenMindat/wiki/GeomaterialIdRetriever)<br>- [GeomaterialDictRetriever()](https://github.com/ChuBL/OpenMindat/wiki/GeomaterialDictRetriever) |   Search query to return information about mindat database items such as id, name, group id etc.    |
| Geomaterial_search | - [GeomaterialSearchRetriever()](https://github.com/ChuBL/OpenMindat/wiki/GeomaterialSearchRetriever)   |   Query to search for mindat database entries based on search keywords.|
| Localities         | - [LocalitiesRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesRetriever)<br>- [LocalitiesIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesIdRetriever) | Search query to return information about different localities, for examples the main elements present in the Jegdalek ruby deposit in Afghanistan |
| Localities_Age     | - [LocalitiesAgeRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesAgeRetriever)<br>- [LocalitiesAgeIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesAgeIdRetriever) |Search query to return locality age details. |
| Localities_Statues | - [LocalitiesStatusRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesStatusRetriever)<br>- [LocalitiesStatusIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesStatusIdRetriever) | Search query to return information about the status type of localities. For example, abandoned is a status type. |
| Localities_Type    | - [LocalitiesTypeRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesTypeRetriever)<br>- [LocalitiesTypeIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesTypeIdRetriever)| Search query to return information about the type of localities. For example, a Mining Field is a locality type.|
| LocGeoregion2      | - [GeoRegionRetriever()](https://github.com/ChuBL/OpenMindat/wiki/GeoRegionRetriever) | Gives information about GeoRegion boundaries |
| LocObject          | - [LocobjectRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocobjectRetriever) | N/A |
| Minerals-IMA       | - [MineralsIMARetriever()](https://github.com/ChuBL/OpenMindat/wiki/MineralsIMARetriever)<br>- [MineralsIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/MineralsIdRetriever) | Search query to return IMA details for a mineral. For example the year it's IMA status was approved. |
| Nickel_Strunz      | - [StrunzRetriever()](https://github.com/ChuBL/OpenMindat/wiki/StrunzRetriever) | Search query to return information about the Nickel-Strunz-10 classification standard.  |
| Photo_Count        | - [PhotoCountRetriever()](https://github.com/ChuBL/OpenMindat/wiki/PhotoCountRetriever) | N/A|

## Use Cases

### 0. Setup

#### Setting API Key in Alternative Ways

```python
import os

os.environ["MINDAT_API_KEY"] = 'Your_Mindat_API_Key'
```

> If you do not have a Mindat API key, please refer to [How to Get My Mindat API Key or Token?](https://www.mindat.org/a/how_to_get_my_mindat_api_key)

You can also set the API key by following the general queries.

#### Checking Available Methods

```python
from openmindat import GeomaterialRetriever

gr = GeomaterialRetriever()
# Print out the available functions for a class
gr.available_methods()
```
```python
from openmindat import GeomaterialRetriever

gr = GeomaterialRetriever()
# Typo check
gr.elements_in('Cu')
'''>>> AttributeError: 'GeomaterialRetriever' object has no attribute 'elements_in', 
Available methods: ['_init_params', 'available_methods', 'bi_max', 'bi_min', 'cleavagetype', 'color', 
'colour', 'crystal_system', 'density_max', 'density_min', 'diaphaneity', 'elements_exc', 'elements_inc', 
'entrytype', 'expand', 'fields', 'fracturetype', 'get_dict', 'groupid', 'hardness_max', 'hardness_min', 
'id__in', 'ima', 'ima_notes', 'ima_status', 'lustretype', 'meteoritical_code', 
'meteoritical_code_exists', 'name', 'non_utf', 'omit', 'optical2v_max', 'optical2v_min', 'opticalsign', 
'opticaltype', 'ordering', 'page', 'page_size', 'polytypeof', 'q', 'ri_max', 'ri_min', 'save', 'saveto', 
'streak', 'synid', 'tenacity', 'updated_at', 'varietyof']. Did you mean: 'elements_inc'?'''
```

### 1. Perform Detailed Queries on Geomaterials

```python
from openmindat import GeomaterialRetriever

gr = GeomaterialRetriever()
gr.density_min(2.0).density_max(5.0).crystal_system("Hexagonal")
gr.elements_exc("Au,Ag")
gr.save()
```

### 2. Retrieve IMA-Approved Minerals

```python
from openmindat import MineralsIMARetriever

mir = MineralsIMARetriever()
mir.fields("id,name,ima_formula,ima_year")
mir.saveto("./mindat_data", 'my_filename')
```

### 3. Search Geomaterials Using Keywords

```python
from openmindat import GeomaterialSearchRetriever

gsr = GeomaterialSearchRetriever()
gsr.geomaterials_search("quartz, green, hexagonal")
gsr.save("filename")

# Alternatively, you can get the list object directly:
gsr = GeomaterialSearchRetriever()
gsr.geomaterials_search("ruby, red, hexagonal")
print(gsr.get_dict())
```

### 4. Retrieve Localities

```python
from openmindat import LocalitiesRetriever

# Download Localities for certain state
lr = LocalitiesRetriever()
lr.country("USA").txt("Idaho")
lr.save()

# Alternatively, you can get the list object directly:
lr = LocalitiesRetriever()
lr.country("Canada").description("mine")
print(lr.get_dict())
```

### 5. Retrieve Type Localities for IMA-Approved Mineral Species

```python
from openmindat import GeomaterialRetriever

gr = GeomaterialRetriever()
gr.ima(True).expand("type_localities")
gr.saveto("./mindat_data")
```

### 6. Retrieve Locality Occurrences for Single Mineral Species
Please consider using only one mineral species ID for querying localities occurrences since this query might result in many records and exceed the server limitation.

```python
from openmindat import GeomaterialRetriever

gr = GeomaterialRetriever()
gr.expand("locality").id__in(str(id_value))
gr.saveto("./mindat_data")
```

## Documentation and Links

- [Get your Mindat API Key](https://www.mindat.org/a/how_to_get_my_mindat_api_key)
- [GitHub Wiki](https://github.com/ChuBL/OpenMindat/wiki)
- [API Documentation](https://api.mindat.org/v1/schema/redoc/)
- [Geomaterial Fields Definition](https://github.com/smrgeoinfo/How-to-Use-Mindat-API/blob/main/geomaterialfields.csv)
- [R package for OpenMindat](https://github.com/quexiang/OpenMindat)

- **Built-in Help**:

To explore detailed class and method documentation within the OpenMindat package, use Python's built-in `help()` function. This provides direct access to docstrings, showcasing usage examples and parameter details. Example:

```python
from openmindat import GeomaterialRetriever

help(GeomaterialRetriever)
```

The help() is also available for the specific functions:

```python
from openmindat import MineralsIMARetriever

help(MineralsIMARetriever.fields)
```

Press `q` to exit the help interface.


## Contact Us

For further assistance or feedback, feel free to contact the development team at [jiyinz@uidaho.edu](mailto:jiyinz@uidaho.edu).


## License

**Project Licence:** [Apache](LICENSE)

**Mindat Data License:** [CC BY-NC-SA 4.0 DEED](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en)

The Mindat API is currently in beta test, and while access is free for all, please note that the data provided are not yet licensed for redistribution and are for private, non-commercial use only. Once launched, data will be available under an open-access license, but please always check the terms of use of the license before reusing these data.

## Authors

Jiyin Zhang, Cory Clairmont, Xiaogang Ma

## Citations

If you use the data or code from this repository, please cite it as indicated below.

```
@misc{OpenMindat,
  author = {Jiyin Zhang and Cory Clairmont and Xiaogang Ma},
  title = {OpenMindat: A Python Package for Geomaterial Data Analysis and Retrieval from Mindat API},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/ChuBL/OpenMindat}},
  note = {Version 0.0.8}
}
```

Additionally, you should also reference the following paper:

Ma, X., Ralph, J., Zhang, J., Que, X., Prabhu, A., Morrison, S.M., Hazen, R.M., Wyborn, L. and Lehnert, K., 2024. *OpenMindat: Open and FAIR mineralogy data from the Mindat database*. *Geoscience Data Journal*, 11(1), pp.94-104. [https://doi.org/10.1002/gdj3.204](https://doi.org/10.1002/gdj3.204).



## Acknowledgments

<p float="left">
        <img src="https://raw.githubusercontent.com/ChuBL/OpenMindat/main/figures/mindat2017.png"  width="25%">
        <img src="https://raw.githubusercontent.com/ChuBL/OpenMindat/main/figures/NSF_Official_logo_Low_Res.png"  width="10%">
</p>

- This work is supported by NSF, Award #2126315.

## Change Logs


[View the full changelog here](https://github.com/ChuBL/OpenMindat/blob/main/CHANGELOG.md)
