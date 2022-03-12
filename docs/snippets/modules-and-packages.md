# :Moonleap-modules and :Moonleap-packages

## Snippet (`bar_pkg/__init__.py`)

```
from . import graphqlapi, mutation, query

modules = [
    graphqlapi,
    item,
    itemlist,
]
```

## Fact

A :Moonleap-module contains the Python code that is related to a particular :resource. Here, we have :Moonleap-modules `graphqlapi`, `item` and `itemlist`.

## Fact

A :Moonleap-package is a Python package that contains several :Moonleap-modules. Here, we have :Moonleap-package `bar_pkg`.

## Fact

The init file of a :Moonleap-package has a `modules` variable that lists all the modules in the :Moonleap-package.
