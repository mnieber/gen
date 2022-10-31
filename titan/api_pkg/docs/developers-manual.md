# Purpose

The api_pkg allows you to specify the data-model that is used by the various services
in your project, as well as the queries and mutations that work against this data-model.

## Snippet (./specs/foo/spec.rst)

```
# The todos:module

The todos:module /provides the todo:item~list.
```

## Fact: the :item~list resource represents a list of items

Similarly, the :item resource represents a single item of some type, e.g. `todo:item`.
An :item has a `name` that we shall refer to as the `item-name`.

## Snippet (./specs/foo/spec.rst)

```yaml
# models.yaml

server:
  todolists.todolist:
    '__type__': entity.sorted
    'name': String.255.display

    todos.todoSet=_@>:
      'isCompleted': Boolean = False
      'name': String.255.display
```

## Fact: :TypeSpecs are loaded from models.yaml

The TypeSpec class describes the fields of an :item. If `TypeSpec.is_form` is true, the then `TypeSpec` describes the fields that are needed to create an instance of that type.

## Fact: In the root we declares host names, and below we declare :TypeSpecs.

In the example, the host is "server". Below "server", we declare the todolists.todolist type.

## Fact: A type name can be prefixed with a module name

In our example, the module name for `todolists.todolist` is `todolists`, and for `todos.todoSet` it's `todos`.
Module names are simply a way to place different types in the same group.

## Fact: A type spec contains key/value pairs

Here, the `todolist` type has keys `name` and `todos.todoSet=_@>`. It also has `__type__` as a special key (every special key starts with a double underscore).

## Fact: The `__type__` special key declares further details of a type spec

Here, we see from the value for the `__type__` key that the `todolist` type is a sorted entity. Instead of using `__type__`, you can also add special symbols to the type name. Here, the "@" symbol is used to indicate that `todo` is an entity and ">"
indicates that it is sorted.

## Fact: A type spec can declare scalar fields

If the value for a key is not a yaml dict (or "pass", which is a special value that denotes an empty yaml dict), then it's part of a scalar field. In our example, the `todolist` type has `name` as a scalar field. The value for a scalar field starts with the (scalar) type-name, followed by some attributes. In our case, the attributes are `255` (which means that the maximum string length is 255) and `display` (which means that this field is used to display the type in - for example - a list-view).

## Fact: A type spec can declare relational fields

If the value for a key is a yaml dict (or "pass"), then it's part of a relational field. A relational field can be of type `fk`, `relatedSet` or `form`. If the type name ends with "Set" then this indicates a `relatedSet` field. If it ends with "Form" then it indicates a `form` field. Otherwise, it's an `fk` field. In our example, the `todolist` type has `todoSet` as a relational field of type `relatedSet`.

## Fact: A relational fields has a target type

Every key of a relational field indicates a type that is targetted by that field. The value of a relational field is treated as a specification of the target type. In our example, the `todolist` has a `todoSet` field that targets the `todo` type. Note that the notation `todoSet` represents several things at the same time: the target type (`todo`), the relational field type (`relatedSet`) and the field-name `todoSet`. As we shall see later, it's also possible to use a different field-name.

## Fact: A `relatedSet` field implies a related `fk` field on the target type.

In our example, we declared that `todolist` has a `todoSet` field. This is a `relatedSet` that targets `todo`. All of this implies that `todo` has an `fk` relational field that targets `todolist`. You don't need to add this related `fk`, it will be added automatically to `todo` as follows: `todolist: pass.auto.optional.related_fk`. What this says is that `todolist` is an automatic optional `fk` field that targets `todolist`.

## Fact: :Queries and :Mutations are loaded from qml.yaml

- the `query` resource represents a graphql query, e.g. `the get-person:query`.
- the `mutation` resource represents a graphql mutation, e.g. `the save-person:mutation`.

## Field types

Possible field types that can be used in a field spec are:

- `string`, `date`, `boolean`, `slug`, `url`, `uuid` and other scalar types
- `fk`: this field represents an external instance of some item.
- `related set`: this field represents a list of external instances of some item.
- `form`: this field is used in the inputs-type spec of a mutation.

If the field spec does not have a scalar type then it has an associated `target` attribute that
indicates the item-name that is associated with the field. For example, a `fk` with `target`
equal to `Person` returns a `person:item`, a `relatedSet` with this target returns a `person:item~list`
and a `form` with this target is used to create a `person:item`. A field spec of type `uuid` may also
have a `target` attribute.

# Queries

Queries and mutations are loaded from the 'gql.yaml' file.

# Pipelines

A pipeline specifies a route from an input (which can be an item, item~list, query or mutation) to an output (which can be an item or item~list).

# States and containers

A state is a collection of containers.
Every container stores one or more named items or item~lists.

```

```
