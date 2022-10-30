Purpose
=======

The api_pkg allows you to specify the data-model that is used by the various services
in your project, as well as the queries and mutations that work against this data-model.


Items, lists, queries and mutations
===================================

To tell Titan about the data model, you need to declare items, item~lists, queries and mutations:

- the `item` resource represents a single item of some type, e.g. `person:item`.
- the `item~list` resource represents a list of items, e.g. `person:item~list`.
- the `query` resource represents a graphql query, e.g. `the get-person:query`.
- the `mutation` resource represents a graphql mutation, e.g. `the save-person:mutation`.

An `item` has a `name` that we shall refer to as the `item-name`. An `item` has a `type-spec` that describes the fields of the type. It also has a `form-type-spec` that describes the fields that are needed to create a new item of that type.

Type specs
==========

Type specs and field specs are loaded from the `models.yaml` file.

Field types
-----------

Possible field types that can be used in a field spec are:

- `string`, `date`, `boolean`, `slug`, `url`, `uuid` and other scalar types
- `fk`: this field represents an external instance of some item~type.
- `related set`: this field represents a list of external instances of some item~type.
- `form`: this field is used in the inputs-type spec of a mutation.

If the field spec does not have a scalar type then it has an associated `target` attribute that
indicates the item-name that is associated with the field. For example, a `fk` with `target`
equal to `Person` returns a `person:item`, a `relatedSet` with this target returns a `person:item~list`
and a `form` with this target is used to create a `person:item`. A field spec of type `uuid` may also
have a `target` attribute.

Queries
=======

Queries and mutations are loaded from the 'gql.yaml' file.

Pipelines
=========

A pipeline specifies a route from an input (which can be an item, item~list, query or mutation) to an output (which can be an item or item~list).

States and containers
=====================

A state is a collection of containers.
Every container stores one or more named items or item~lists.

