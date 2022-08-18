Purpose
=======

The api_pkg allows you to specify the data-model that is used by the various services
in your project, as well as the queries and mutations that work against this data-model.


Items, lists, queries and mutations
===================================

To tell Titan about the data model, you need to declare items, item~lists, queries and mutations:

- the `item` resource represents a single item of some type, e.g. `person:item`.
- the `item~list` resource represents a list of items, e.g. `person:item~list`.
- the `query` resource represents a graphql query, e.g. `the get-person:query /provides a person:item~list`.
- the `mutation` resource represents a graphql mutation, e.g. `the save-person:mutation /posts a person:item`.

An `item` has a `name` that we shall refer to as the `item-name`. An `item` has a `type-spec` that describes the fields of the type. It also has a `form-type-spec` that describes the fields that are needed to create a new item of that type.

Type specs
==========

We can use the above terms to tell Titan which items, queries and mutations exist, but to generally
useful code, we also need to specify which fields exist on these items. This is done by declaring
type specs. These are JSON-schema data-structures that contain type information.

- a `data-type spec` describes the fields of an item~type
- a `form-type spec` describes the fields of an item~form-type
- an `inputs-type spec` describes the input fields of a `query` or `mutation`
- an `outputs-type spec` describes the output fields of a `query` or `mutation`

All JSON schemas for your project are stored in the type specs directory, which is a subdirectory of
the spec dir. Every schema uses a filename that is based on either an item-name (e.g. `Person.json` for a
data-type spec and `PersonForm.json` for a form-type spec) or a query/mutation name
(e.g. `GetPersonInputs.json`).



Field specs
===========

Every type spec contains so-called field specs. A field spec is a dictionary that describes a field.
It has:

- a name
- a field type
- field attributes (e.g. "required", "unique")

Field types
-----------

Possible field types that can be used in a field spec are:

- `string`, `date`, `boolean`, `slug`, `url`, `uuid` and other scalar types
- `foreignKey`: this field represents an external instance of some item~type.
- `related set`: this field represents a list of external instances of some item~type.
- `form`: this field is used in the inputs-type spec of a mutation.

If the field spec does not have a scalar type then it has an associated `target` attribute that
indicates the item-name that is associated with the field. For example, a `foreignKey` with `target`
equal to `Person` returns a `person:item`, a `relatedSet` with this target returns a `person:item~list`
and a `form` with this target is used to create a `person:item`. A field spec of type `uuid` may also
have a `target` attribute.

Note that if a "foreignKey" field spec in a data-type spec has a "relatedName" field, then a related set field (with the given name) is created on the type spec that it targets. If you set `relatedName: true`, then a default name will be used for the related set field.

Queries
=======

You can tell Titan which queries exist by mentioning them in the spec file, e.g.
`the get-person:query /provides a person:item`.
The default outputs-type spec for a query (which is used if you don't provide one) has a "foreignKey" field for
any item that the query provides, and a "relatedSet" for any item~list that it provides.
Queries also need inputs, and these are described in the inputs-type spec. Titan can create a default
inputs-type spec by - again - looking at the items and item~lists that are provided by the query.
It looks up the `queryItemBy` and `queryItemsBy` values for these items and item~lists to determine the fields of the
default inputs-type spec. The `queryItemBy` for a provided item is stored in the data-type spec of that item.
By default, `queryItemBy` equals ["id"] and `queryItemsBy` equals [] (the empty list).


Mutations
=========

The information about mutations also comes from the spec file, e.g. `the save-person:mutation /posts a person:item`).
Mutations can return items and item~lists, e.g. `the save-person:mutation /returns a person:item`.

Every mutation has a single endpoint that takes a form~type argument for every item that the mutation receives.
These form~type arguments are described as "form" fields in the inputs-type spec for the mutation. Every
form field has a `target` attribute that identifies the form-type. For example, if `target` is `person` then
the field refers to an instance of the `PersonForm.json` type spec. If you don't supply the `PersonForm.json`
type spec, then a default one is created that is based on the fields of the associated `Person.json` type spec.

A mutation has an outputs-type spec that has a "success" flag and an "errors" dictionary. It also has a
foreignKey field for any item that the mutation returns, and a relatedSet for any item~list that it returns.


Case 1: a spec file declares item-types, items and item-lists
=============================================================

The example
-----------

.. code-block:: markdown

    ## The todos:module (todo:x)

    The todos:module /provides the todo:item~list.


.. code-block:: JSON

    # This is an example JSON schema for the Todo type.

    # specs/todoapp/type_specs/Todo.json

    {
        "required": ["id", "name"],
        "queryBy": ["id"],
        "fields": {
            "id": {"type": "uuid"},
            "name": {"type": "string", "maxLength": 255, "unique": true},
            "todolist": {
                "type": "foreignKey",
                "target": "todolist",
                "onDelete": "cascade",
                "relatedName": "+"
            }
        }
    }


Case 2: modules can store item-lists
====================================

The `item` and `item~list` resources can be used in various (frontend and backend) services.
Typically, these services are divided in modules, where different modules work with different
data types. Therefore, a common pattern is to declare in the spec file that the `todos:module`
stores the `todo:item~list`. In case that the spec describes a django module
(e.g. `titan/django_pkg/module`) this would have the effect that the `todos` Django module
would contain a `Todo` django model.

The example
-----------

.. code-block:: python

    # generated Django models file: backend/todos/models.py

    class Todo(Model):
        id = models.Charfield(max_length=255)
        name = models.CharField(max_length=255)
        todolist = models.ForeignKey(Todolist, null=True, blank=True)


Case 3: a spec file declares queries
====================================

The example
-----------

.. code-block:: markdown

    (this is an example spec file)
    The graphql:api /has a todos:query that /provides the todo:item~list.

.. code-block:: markdown

    (the same example, using a shorthand notation)
    The graphql:api /loads the todo:item~list.

.. code-block:: python

    # generated file backend/api/query/todosquery

    class TodosQuery(Model):
        # The `todos` field of type graphene.List is added based on the outputs type spec
        # of the `todos:query`.
        # The TodoType is a graphql type that is based on the todo type spec. The TodoType is
        # used because the outputs type spec contains a foreign key to the todo type.
        # The `todolist_name` argument is added based on the "queryItemsBy" of the todo type spec.
        todos = graphene.List(TodoType, todolist_name=graphene.String())

        def resolve_todos(self, info, todolist_name: string):
            return Todo.objects.filter(todolist__name=todolist_name)


Case 4: a spec file declares mutations
======================================

The example
-----------

.. code-block:: python

    class BarMutation(Model):
        class Arguments:
            # Since the spec declares that a bar:mutation /posts a todo:item, the list of arguments
            # is derived from the 'todo' type spec. Note that the 'todolist' (foreign key) field of this
            # type spec is represented here as the 'todolist_id' field.
            id = graphene.String(required=True)
            name = graphene.String(required=True)
            todolist_id = graphene.String(required=True)

        ok = graphene.Boolean()
        errors = graphene.Any()

        def mutate(self, info, id, name, todolist_id):
            Todo.objects.update_or_create(id=id, defaults=dict(name=name, todolist_id=todolist_id)
            return FooBarQuery(
                ok=True,
                errors=[]
            )
