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
    - [7. Download Mineral Species with Their Locality Records](#7-download-mineral-species-with-their-locality-records)
    - [8. Retrieve Locality Name Translations](#8-retrieve-locality-name-translations)
    - [9. List the Values of a Geomaterial Field](#9-list-the-values-of-a-geomaterial-field)
  - [Errors and Large Queries](#errors-and-large-queries)
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
pip install openmindat
```

OpenMindat requires Python 3.10 or later.

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
| Geomaterials       |  - [GeomaterialRetriever()](https://github.com/ChuBL/OpenMindat/wiki/GeomaterialRetriever)<br>- [GeomaterialIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/GeomaterialIdRetriever)<br>- [GeomaterialDictRetriever()](https://github.com/ChuBL/OpenMindat/wiki/GeomaterialDictRetriever) |   Search query to return information about mindat database items such as id, name, group id etc.    |
| Geomaterial_search | - [GeomaterialSearchRetriever()](https://github.com/ChuBL/OpenMindat/wiki/GeomaterialSearchRetriever)   |   Query to search for mindat database entries based on search keywords.|
| Localities         | - [LocalitiesRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesRetriever)<br>- [LocalitiesIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesIdRetriever) | Search query to return information about different localities, for examples the main elements present in the Jegdalek ruby deposit in Afghanistan |
| Localities_Age     | - [LocalitiesAgeRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesAgeRetriever)<br>- [LocalitiesAgeIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesAgeIdRetriever) |Search query to return locality age details. |
| Localities_Status  | - [LocalitiesStatusRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesStatusRetriever)<br>- [LocalitiesStatusIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesStatusIdRetriever) | Search query to return information about the status type of localities. For example, abandoned is a status type. |
| Localities_Type    | - [LocalitiesTypeRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesTypeRetriever)<br>- [LocalitiesTypeIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/LocalitiesTypeIdRetriever)| Search query to return information about the type of localities. For example, a Mining Field is a locality type.|
| Locality_Translations | - LocalityTranslationsRetriever()<br>- LocalityTranslationsIdRetriever() | Locality names in other languages, e.g. the French name of a locality. |
| Minerals-IMA       | - [MineralsIMARetriever()](https://github.com/ChuBL/OpenMindat/wiki/MineralsIMARetriever)<br>- [MineralsIdRetriever()](https://github.com/ChuBL/OpenMindat/wiki/MineralsIdRetriever) | Search query to return IMA details for a mineral. For example the year it's IMA status was approved. |
| Nickel_Strunz      | - [StrunzRetriever()](https://github.com/ChuBL/OpenMindat/wiki/StrunzRetriever) | Search query to return information about the Nickel-Strunz-10 classification standard.  |

`DanaRetriever` and `StrunzRetriever` need a sub-listing or an id, e.g. `DanaRetriever().groups()` or `StrunzRetriever().classes()`. The Mindat API has no plain list for these endpoints.

The Mindat API no longer provides the countries, locgeoregion2, locobject and photocount endpoints. For old code, `CountriesListRetriever`, `CountriesIdRetriever`, `GeoRegionRetriever`, `LocobjectRetriever` and `PhotoCountRetriever` can still be imported from their modules (e.g. `openmindat._countries`), but they raise `EndpointUnavailableError` when queried. They will be removed in version 0.2.0.

## Use Cases

### 0. Setup

#### Setting Your API Key

If you do not have a Mindat API key yet, see [How to Get My Mindat API Key or Token?](https://www.mindat.org/a/how_to_get_my_mindat_api_key). Then use one of these options:

```python
# Option 1: environment variable (good for scripts and CI)
import os
os.environ["MINDAT_API_KEY"] = "Your_Mindat_API_Key"

# Option 2: save the key once for later sessions
import openmindat
openmindat.set_api_key("Your_Mindat_API_Key", persist=True)
```

Option 3: just run a query. If no key is found, OpenMindat asks for one and saves it.

A saved key is stored in `~/.config/openmindat/credentials.yaml` (`%APPDATA%\openmindat\credentials.yaml` on Windows), readable only by you. If you used OpenMindat 0.1.3 or earlier, the `.apikey.yaml` file in your working folder is still read, and it is copied to the new location automatically.

To check which key is used and whether Mindat accepts it:

```python
import openmindat

print(openmindat.api_key_status())
# Mindat API key abcd…wxyz from env: valid
```

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
'colour', 'crystal_system', 'density_max', 'density_min', 'diaphaneity', 'diapheny', 'el_essential', 
'el_exc', 'el_inc', 'elements_exc', 'elements_inc', 'entrytype', 'expand', 'fields', 'fracturetype', 
'get_dict', 'groupid', 'hardness_max', 'hardness_min', 'id_in', 'id_max', 'id_min', 'ima', 'ima_notes', 
'ima_status', 'lustretype', 'meteoritical_code', 'meteoritical_code_exists', 'name', 'non_utf', 'omit', 
'optical2v_max', 'optical2v_min', 'opticalsign', 'opticaltype', 'ordering', 'page', 'page_size', 
'polytypeof', 'q', 'ri_max', 'ri_min', 'save', 'saveto', 'streak', 'synid', 'tenacity', 'updated_at', 
'varietyof', 'verbose']. Did you mean: 'elements_inc'?'''
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
mir.saveto("./mindat_data", 'my_filename')

# Filters work as on GeomaterialRetriever, e.g. hexagonal minerals with hardness >= 8:
mir = MineralsIMARetriever()
mir.crystal_system("Hexagonal").hardness_min(8)
print(mir.get_dict())
```

> `MineralsIMARetriever().fields(...)` currently fails when the field list includes `name`. This is a Mindat server issue that has been reported.

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

# Only the exact name match:
gsr = GeomaterialSearchRetriever()
gsr.geomaterials_search("quartz").e(1)
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

# Localities in Norway at the top two hierarchy levels with at least 10 sub-localities,
# including the ids of their minerals:
lr = LocalitiesRetriever()
lr.country("Norway").level_lte(2).sublocs_gte(10).expand("geomaterials")
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
gr.expand("locality").id_in("3337")  # 3337 is Quartz
gr.saveto("./mindat_data")
```

### 7. Download Mineral Species with Their Locality Records

`expand("locality")` adds the ids of every locality where a mineral is recorded on Mindat. It is the usual starting point for a mineral occurrence dataset. Include `locality` in `fields`; otherwise it is dropped from the output.

```python
from openmindat import GeomaterialRetriever, LocalitiesRetriever

# The first 5 IMA-approved minerals with their locality ids
gr = GeomaterialRetriever()
gr.ima(True).expand("locality").fields("id,name,ima_formula,locality")
gr.page_size(5).page(1)
minerals = gr.get_dict()["results"]

for m in minerals:
    print(f"{m['name']:<20} {len(m['locality']):>5} localities")
```

To turn the locality ids into names and coordinates, look them up with `LocalitiesRetriever().id_in(...)`. Query in batches of about 200 ids: common minerals have thousands of localities, which is too long for a single request.

```python
mineral = minerals[2]  # Abernathyite
ids = mineral["locality"]

localities = []
for start in range(0, len(ids), 200):
    batch = ",".join(map(str, ids[start:start + 200]))
    lr = LocalitiesRetriever().id_in(batch).fields("id,txt,latitude,longitude")
    localities += lr.get_dict()["results"]

for loc in localities:
    print(loc["id"], loc["latitude"], loc["longitude"], loc["txt"])
```

Mindat stores "no coordinates" as `latitude = longitude = 0.0` (typically for regions such as countries or districts), not as empty values.

To download all IMA-approved minerals with their locality ids, remove `.page(1)` and save to a file. This covers about 6,200 minerals and over one million mineral–locality pairs (about 25 MB), so it takes a while:

```python
gr = GeomaterialRetriever()
gr.ima(True).expand("locality").fields("id,name,ima_formula,locality").page_size(50)
gr.saveto("./mindat_data", "minerals_with_localities")
```

### 8. Retrieve Locality Name Translations

```python
from openmindat import LocalityTranslationsRetriever

# French names of locality 14090 (Belgium)
ltr = LocalityTranslationsRetriever()
ltr.lt_loc(14090).lt_iso("fr")
print(ltr.get_dict())
```

### 9. List the Values of a Geomaterial Field

```python
from openmindat import GeomaterialDictRetriever

# All crystal systems used by Mindat. field() is required.
gdr = GeomaterialDictRetriever()
print(gdr.field("csystem").get_dict())
```

## Errors and Large Queries

When the Mindat API cannot answer a query, OpenMindat raises an exception. Each one is also a `ValueError`, so existing `except ValueError:` code keeps working.

| Exception | Raised when |
|---|---|
| `MindatRequestError` | The Mindat API rejected the request (HTTP 4xx), e.g. an unknown id or a missing parameter. The message quotes the server's reason. |
| `MindatServerError` | The Mindat server failed: an HTTP 5xx error, a gateway timeout, a rate limit or a network problem. |
| `EndpointUnavailableError` | The class wraps an endpoint the Mindat API no longer provides. |

```python
from openmindat import GeomaterialRetriever, MindatServerError

gr = GeomaterialRetriever().ima(True).crystal_system("Monoclinic").expand("locality")
try:
    data = gr.get_dict()
except MindatServerError as error:
    print(error)
    data = {"results": error.partial_results}  # records downloaded before the failure
```

To get error responses back as data instead, as in version 0.1.3 and earlier, set `openmindat.MindatApi.RAISE_HTTP_ERRORS = False`.

Large queries are downloaded in pages of 1500 records. If the server times out on a page, OpenMindat requests that page again in smaller pieces, and it waits when the server asks it to slow down. To make big downloads faster, request only the fields you need. For example, `GeomaterialRetriever().fields("id,name,mindat_formula")` made pages about 25 times smaller in our tests.

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
  note = {Version 0.1.4}
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
