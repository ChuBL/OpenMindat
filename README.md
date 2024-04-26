# OpenMindat Python Package

This is a test version of the OpenMindat Python package, designed to facilitate querying and retrieving data on minerals and geomaterials from the Mindat API. It provides classes for detailed queries based on various attributes like IMA status, keywords, and specific geomaterial properties.

GitHub Repository: [OpenMindat Python Package](https://github.com/ChuBL/OpenMindat)

## Get Started

### Install via Pip

```console
foo@bar:~$ pip install openmindat
```

### Import the Package in Python

```python
import openmindat
```

## Use Cases

### 0. Setting API Key in Alternative Ways

```python
import os

os.environ["MINDAT_API_KEY"] = 'Your_Mindat_API_Key'
```

> If you do not have a Mindat API key, please refer to [How to Get My Mindat API Key or Token?](https://www.mindat.org/a/how_to_get_my_mindat_api_key)

You can also set the API key by following the general queries.

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

:exclamation: Some country names, e.g., United States and United Kingdom, are not working due to server-side problems, which will be fixed in the future.

```python
from openmindat import LocalitiesRetriever

lr = LocalitiesRetriever()
lr.country("France").txt("mine")
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

## Documentation

- **GitHub Wiki**: For comprehensive documentation, visit our [GitHub Wiki](https://github.com/ChuBL/OpenMindat/wiki).

- **OpenMindat API Documentation**:
  [OpenMindat Redoc](https://api.mindat.org/schema/redoc/)

- **Built-in Help**:

To explore detailed class and method documentation within the OpenMindat package, use Python's built-in `help()` function. This provides direct access to docstrings, showcasing usage examples and parameter details. Example:

```python
from openmindat import GeomaterialRetriever

help(GeomaterialRetriever)
```

The help() is also available for the specific functions:

```python
>>> from openmindat import MineralsIMARetriever

>>> help(MineralsIMARetriever.fields)
```

Press `q` to exit the help interface.



### Contact Us

For further assistance or feedback, feel free to contact the development team at [jiyinz@uidaho.edu](mailto:jiyinz@uidaho.edu).


## License

**Project Licence:** [Apache](LICENSE)

**Mindat Data License:** [CC BY-NC-SA 4.0 DEED](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en)

The Mindat API is currently in beta test, and while access is free for all, please note that the data provided are not yet licensed for redistribution and are for private, non-commercial use only. Once launched, data will be available under an open-access license, but please always check the terms of use of the license before reusing these data.

## Author

Jiyin Zhang, Clairmont Cory

## Acknowledgments

<p float="left">
        <img src="https://github.com/ChuBL/OpenMindat/blob/main/Logo/mindat2017.png?raw=true"  width="25%">
        <img src="https://github.com/ChuBL/OpenMindat/blob/main/Logo/NSF_Official_logo_Low_Res.png?raw=true"  width="10%">
</p>

- This work is supported by NSF, Award #2126315.

## Upgrading Logs

### 0.0.5
**Released:** Apr 26, 2024

- The `Internal Server Error` issue in v0.0.4 is fixed from the server side.
- The get functions are now changed to `get_dict`.
- Added progress bars for multiple-page queries.
- Some other minor updates.


### 0.0.4
**Released:** Apr 14, 2024

- Tentative issue: Data queries involving multiple pages might return an `Internal Server Error` due to server-end issues. [Related GitHub issue](https://github.com/ChuBL/OpenMindat/issues/12)
- Added support to getting list objects of obtained data in addition to saving it to local directories.

### 0.0.3
**Released:** Apr 11, 2024

- Tentative issue: Data queries involving multiple pages might return an `Internal Server Error` due to server-end issues. 
- Now supporting more Mindat endpoints. Not fully tested. Feedback is welcome.
- Revised API key obtaining workflow.

### 0.0.1
**Released:** Dec 14, 2023

- Initial release of the package.
