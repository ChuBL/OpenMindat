# OpenMindat
A test version for OpenMindat Python package.

# Get Started

1. `Download` or `Clone` this repository to your DIR
For example:
```console
/Your_Dir/
```
2. `Install` the package in your terminal
```console
foo@bar:~$ cd /Your_Dir/OpenMindat/
foo@bar:OpenMindat$ pip install .
```
3. `Import` the package in Python

```python
import openmindat as om
```

# Use Cases

1. Get the IMA minerals

```python
import openmindat as om

om.get_ima_minerals()
```

2. Get arbitrary geomaterials

```python
import openmindat as om

# Test1
om.get_geomaterials()

# Test2
# set your selected fields here
fields_str = 'id,name,mindat_formula'

params = {
        'fields': fields_str, # put your selected fields here
        'format': 'json'
    }
om.get_geomaterials(params)
```