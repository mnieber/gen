# Purpose

The api_pkg allows you to specify the data-model that is used by the various services
in your project, as well as the queries and mutations that work against this data-model.

## Item declarations in the spec fo;e

### Snippet (./specs/foo/spec.rst)

```
# The todos:module

The todos:module /provides the todo:item~list.
```

### The spec file can declare items and item-lists

The :item resource represents a single item of some type, e.g. `todo:item`.
Similarly, the :item~list resource represents a list of items.
An :item has a `name` that we shall refer to as the `item-name`.

### Next: loading type-specs

We've seen now how an item or item-list is declared. Next, we will look at how an item's
data-type is defined.

## Type specifications in the models.yaml file

### Snippet

```yaml
# models.yaml

server:
  todolists.todolist:
    '__type__': entity.sorted
    'name': String.255.display

    todos.todoSet=[@>]:
      'isCompleted': Boolean = False
      'name': String.255.display
```

### :type-spec are loaded from models.yaml

A :type-spec instance describes the fields of an :item. :Type-specs are defined in the `models.yaml` file.

### The root of `models.yaml` contains host names, below which we declare :type-specs.

In a software system, it's often the case that the same type is used in different services. However, each service
may use a slightly different variantion of the type. Therefore, :type-specs are declared respective to a particular
service. In the example, the service is called `server`, and it uses the `todolists.todolist` type. Later, we will
add a `client` service that uses a slightly different `todolist` :type-spec.

### A type name can be prefixed with a module name

We've used a name for our :type-spec that is comprised of two parts (which are separated by a dot): the module
name (`todolists`) and the type-spec name (`todolist`). This allows us to split the :type-specs into modules.

### A :type-spec contains :scalar-fields and :relational-fields, which are key/value pairs

The `todolist` :type-spec has two normal keys (`name` and `todos.todoSet=[@>]`) and one :special-key: `__type__`.
The `name` key belongs to what is called a :scalar-field. The `todos.todoSet=[@>]` key refers to another type-spec and belongs to a so-called :relational-field. The symbols at the end of our :relational-field key (such as `@`) are explained later.

## :Relational-fields

### Snippet

```yaml
# models.yaml

server:
  todolists.todolist:
    '__type__': entity.sorted
    'name': String.255.display

    todos.todoSet=[@>]:
      'isCompleted': Boolean = False
      'name': String.255.display
```

### Every :relational-field has a dict value (or "pass")

If the value for a key is a yaml dict (or the special value "pass", which represents and empty dict), then it's part of a
:relational-field. A relational field can be of type `fk`, `relatedSet` or `form`. If the type name ends with "Set" then this indicates a `relatedSet` field. If it ends with "Form" then it indicates a `form` field. Otherwise, it's an `fk` field. In our example, the `todolist` type has `todoSet` as a relational field of type `relatedSet`.

### Every :relational-field has a target type

Every key of a relational field indicates a type that is targetted by that field. The value of a relational field is treated as a specification of the target type. In our example, the `todolist` has a `todoSet` field that targets the `todo` type. Note that the notation `todoSet` represents several things at the same time: the target type (`todo`), the relational field type (`relatedSet`) and the field-name `todoSet`. As we shall see later, it's also possible to use a different field-name.

### A :relational-field key can have symbols

The symbols at the end of a :relational-field key represent attributes of target :type-spec. Here, the "@" symbol is used to indicate that `todo` is an entity and ">" indicates that it is sorted.

### The `__type__` special key stores attributes of a :type-spec.

Instead of using symbols, you can also specify the attributes of the target :type-spec using the `__type__` special key.
Here, we see from the value for the `__type__` key that the `todolist` type is a sorted entity.

## Fact: A `relatedSet` field implies a related `fk` field on the target type.

For technical reasons (that have to do with relational databases), when we declare that `todolist` has a `todoSet` field then we also need a related `fk` field on `todo` that targets `todolist`. This related `fk` will be added automatically to `todo` as follows: `todolist for todoSet: pass.auto.optional`. The `for` clause identifies the related field name in the parent type. The `auto` attribute indicates an automatically added field. If you also manually specify the `todolist` field in the `todo` type, then the automatically added field is ignored.

## Scalar fields

## Every :scalar-field has a string value.

If the value for a key is not a yaml dict (or "pass"), then it's part of a scalar field. In our example, the `todolist` type has `name` as a scalar field. The value for a scalar field starts with the (scalar) type-name, followed by some attributes. In our case, the attributes are `255` (which means that the maximum string length is 255) and `display` (which means that this field is used to display the type in - for example - a list-view).

## Form types

### A :TypeSpec can contain a form

If `TypeSpec.is_form` is true, the then `TypeSpec` describes the fields that are needed to create an instance of that type.

## Declaring type variations for the `client` service

### Snippet

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

### The client host can specify variations on types

Here, we see that the "client" host uses the `todolist` type with some modifications that are specified using the `__update__` key. The "\*" symbol means that the field is not used at all in the "client" host.

### A field can be marked as "model" or "api"

Some fields are intended to be stored in the data model but not exposed in the api. Other fields do not exist in the model but only in the api (which means that the field needs to be derived from other data). In the above snippet, the `name` field is marked as existing only in the model, and the `description` field as existing only in the api.

### A form type derives from a data type

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
