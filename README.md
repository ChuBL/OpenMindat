# OpenMindat
A test version for OpenMindat Python package.

# Use Cases

1. Get the IMA minerals

```{python}
get_ima_minerals()
```

2. Get arbitrary geomaterials

```{python}
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