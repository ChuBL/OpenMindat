# OpenMindat Python Package

This is a test version of the OpenMindat Python package, designed to facilitate querying and retrieving data on minerals and geomaterials from the Mindat API. It provides classes for detailed queries based on various attributes like IMA status, keywords, and specific geomaterial properties.

GitHub Reposity: [OpenMindat Python Package](https://github.com/ChuBL/OpenMindat)

## Get Started

> If you do not have a Mindat API key, please refer to [How to Get My Mindat API Key or Token?](https://www.mindat.org/a/how_to_get_my_mindat_api_key)

### Install via Pip

```console
foo@bar:~$ pip install openmindat
```

### Import the Package in Python

```python
import openmindat
```

## Use Cases

### 1. Perform Detailed Queries on Geomaterials

```python
from openmindat import GeomaterialRetriever

gr = GeomaterialRetriever()
gr.density_min(2.0).density_max(5.0).crystal_system("Hexagonal")
gr.elements_exc("Au,Ag")
gr.saveto("/path/to/geomaterials_data")
```

### 2. Retrieve IMA-Approved Minerals

```python
from openmindat import MineralsIMARetriever

mir = MineralsIMARetriever()
mir.ima(1).fields("id,name,ima_formula,ima_year")
mir.saveto("/path/to/minerals_data")
```

### 3. Search Geomaterials Using Keywords

```python
from openmindat import GeomaterialSearchRetriever

gsr = GeomaterialSearchRetriever()
gsr.geomaterials_search("quartz, green, hexagonal")
gsr.save()
```

### 4. Retrieve Localities

```python
from openmindat import LocalitiesRetriever

lr = LocalitiesRetriever()
lr.country("France").txt("mine")
lr.save()
```

### 5. Retrieve Type Localities for IMA-Approved Mineral Species

```python
from openmindat import GeomaterialRetriever

gr = GeomaterialRetriever()
gr.ima(True).expand("type_localities")
gr.saveto("/content/sample_data")
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

[Apache](LICENSE)

## Author

Jiyin Zhang, Clairmont Cory

## Acknowledgments

<p float="left">
        <img src="https://github.com/ChuBL/OpenMindat/blob/main/Logo/mindat2017.png?raw=true"  width="25%">
        <img src="https://github.com/ChuBL/OpenMindat/blob/main/Logo/NSF_Official_logo_Low_Res.png?raw=true"  width="10%">
</p>

- This work is supported by NSF, Award #2126315.
