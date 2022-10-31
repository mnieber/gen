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

## Snippet

```yaml
# models.yaml

server:
  todolists.todolist:
    '__type__': entity.sorted
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

Here, the `todolist` type has keys `name` and `todos.todoSet=_@>`. It also has `__type__` as a special key (every special key starts with a double underscore). Here, we see from the value for the `__type__` key that the `todolist` type is a sorted entity.

## Fact: A type spec can declare scalar fields

If the value for a key is not a yaml dict (or "pass", which is a special value that denotes an empty yaml dict), then it's part of a scalar field. In our example, the `todolist` type has `name` as a scalar field. The value for a scalar field starts with the (scalar) type-name, followed by some attributes. In our case, the attributes are `255` (which means that the maximum string length is 255) and `display` (which means that this field is used to display the type in - for example - a list-view).

## Snippet

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

## Fact: Symbols can be used instead of `__type__`

Instead of using `__type__`, you can also add special symbols to the type name. Here, the "@" symbol is used to indicate that `todo` is an entity and ">" indicates that it is sorted.

## Fact: A type spec can declare relational fields

If the value for a key is a yaml dict (or "pass"), then it's part of a relational field. A relational field can be of type `fk`, `relatedSet` or `form`. If the type name ends with "Set" then this indicates a `relatedSet` field. If it ends with "Form" then it indicates a `form` field. Otherwise, it's an `fk` field. In our example, the `todolist` type has `todoSet` as a relational field of type `relatedSet`.

## Fact: A relational fields has a target type

Every key of a relational field indicates a type that is targetted by that field. The value of a relational field is treated as a specification of the target type. In our example, the `todolist` has a `todoSet` field that targets the `todo` type. Note that the notation `todoSet` represents several things at the same time: the target type (`todo`), the relational field type (`relatedSet`) and the field-name `todoSet`. As we shall see later, it's also possible to use a different field-name.

## Fact: A `relatedSet` field implies a related `fk` field on the target type.

For technical reasons (that have to do with relational databases), when we declare that `todolist` has a `todoSet` field then we also need a related `fk` field on `todo` that targets `todolist`. This related `fk` will be added automatically to `todo` as follows: `todolist for todoSet: pass.auto.optional`. The `for` clause identifies the related field name in the parent type. The `auto` attribute indicates an automatically added field. If you also manually specify the `todolist` field in the `todo` type, then the automatically added field is ignored.

## Snippet

```yaml
# models.yaml

server:
  todolists.todolist:
    '__type__': entity.sorted
    'name|': String.255.display
    'description^': String

client:
  todoForm: pass
  todolist:
    '__update__': [name*]
```

## Fact: The client host can specify variations on types

Here, we see that the "client" host uses the `todolist` type with some modifications that are specified using the `__update__` key. The "\*" symbol means that the field is not used at all in the "client" host.

## Fact: A field can be marked as "model" or "api"

Some fields are intended to be stored in the data model but not exposed in the api. Other fields do not exist in the model but only in the api (which means that the field needs to be derived from other data). In the above snippet, the `name` field is marked as existing only in the model, and the `description` field as existing only in the api.

## Fact: A form type derives from a data type

Here, we see a `todoForm` type that can be used to create a `todo` instance.

## Snippet

```yaml
query getTodolists:
  outputs:
    todolists as todolistSet: pass

mutation saveTodo:
  inputs:
    todoForm: pass
  saves: [todo]
```

## Fact: :Queries and :Mutations are loaded from qml.yaml

Here we see a `getTodolists` query that provides a todolistSet.
We also see a `saveTodo` mutation that takes a `todoForm` and saves a `todo`.

# Pipelines

A pipeline specifies a route from an input (which can be an item, item~list, query or mutation) to an output (which can be an item or item~list).

# States and containers

A :state is a collection of :containers.
Every :container stores one or more named :items or :item~lists.
A :state~provider runs a :pipeline and copies the output to its :containers.

# :FormViews

A :FormView has a :pipeline that allows it to run a mutation.
