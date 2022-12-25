# Packages

A `package` is a Python package that describes Moonleap `resources` and `scopes`.
The `install_package` function is used to install the contents of a `package` in the Moonleap runtime.
Every `package` can extend the resources in other `packages` by using `extensions`.
A `scope` is a set of `rules` that applies in some part of the Moonleap spec file.
A `scope manager` manages the collection of available `scopes`.
