# OpenMindat
A test version for OpenMindat Python package.

# Get Start

1. Download or clone this repository to your DIR
For example:
```console
/Your_Dir/
```
2. Install the package in your terminal
```console
cd /Your_Dir/OpenMindat/
pip install .
```
3. Import the package

```python
import openmindat
```

# Use Cases

1. Get the IMA minerals

```python
get_ima_minerals()
```

2. Get arbitrary geomaterials

```python
# Test1
get_geomaterials()

# Test2
# set your selected fields here
fields_str = 'id,name,mindat_formula'

params = {
        'fields': fields_str, # put your selected fields here
        'format': 'json'
    }
get_geomaterials(params)
```