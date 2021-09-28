Purpose
=======

The api_pkg allows you to specify the data-model that is used by the various services
in your project, as well as the queries and mutations that work against this data-model.
Below, the process will be explained using annotated use-cases.

Case 1: a spec file declares item-types, items and item-lists
=============================================================

Description
-----------

The spec file can declare resources that represent item-types, items, and item lists. For example,
when you declare a `todo:item` resource then this resource represents a single instance of the
`todo:item~type`. Similarly, a `todo:item~list` resource represents a list of `todo:item~type`.

Every item-type has two associated type specs called 'data-type spec' and 'form-type spec'.
The data-type spec is used to describe a type that is returned from a query, whereas the the form-type spec
describes a type that posted in a mutation.
Both type specs are formatted as JSON schemas and stored in the type specs directory.

A type spec contains type information including so-called field specs that describe the fields of
the type. The field specs in the JSON schema are dictionaries that have a name and a field type, which can be a
scalar or a foreign key (that points to some type spec). There are two different types of foreign keys:
- fk: this is used when a type references an instance of another type by its id.
- relatedSet: this is used when a type references several instances of another type by their ids. By
  default, when `foo` has a "fk" field that points to `bar`, then a `relatedSet` field (pointing to `foo`)
  is automatically added to `bar`. The exception is when `hasRelatedSet` is set to false in the fk"
  field spec.

If a data-type spec for an item-type does not exist in the type specs directory then a default
one is used that has "name" and "id" field specs. If a form-type spec does not exist in this directory,
then an automatically created type spec based on the associated data-type spec is used.

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
        "private": [],
        "properties": {
            "id": {"type": "uuid"},
            "name": {"type": "string", "maxLength": 255, "unique": true},
            "todolist": {
                "type": "fk",
                "target": "todolist",
                "onDelete": "cascade",
                "hasRelatedSet": true
            }
        }
    }


Case 2: modules can store item-lists
====================================

The `item` and `item~list` resources can be used is various (frontend and backend) services.
Typically, these services are divided modules, where different modules work with different
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

Description
-----------

The spec file can declare a `foo:query` resource that `/provides` a `todo:item` and/or
`todo:item~list`. Moonleap uses this information to generate graphql queries based on the
type specs for these items. To every query corresponds a so-called 'inputs type spec' and
'outputs type spec' that that describe the inputs and outputs for that query.
If the query is named `foo` then these type specs are named `FooInputsType` and
`FooOutputsType`. You can define these type specs in the type-specs directory, and if you
don't then Moonleap creates default ones.

To provide a `todo:item` it must be specified how these items are queried. By default, to query
a single item you need to provide its "id". However, you can override this default using the
`queryItemBy` type spec value. For example, setting `queryItemBy` to `['name']` indicates that
the todo name is used to find the todo.
Similarly, you can use the `queryItemsBy` type spec value to specify how an `item~list` is queried.
For example, to query todos by the todolist name you can set `queryItemsBy` to `[('todolist', 'name')]`.

The default outputs type spec will contain a "fk" field for every item that the query
provides, and a "related_set" field for every item~list that it provides. The final graphql
code that is generated for the `query` resource depends on:
- the in/outputs type spec and the foreign key fields therein.
- the type specs that are associated with these foreign keys.
- the "queryItemBy" and "queryItemsBy" of these assiociated type specs.

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

Description
-----------

The spec file can declare a `bar:mutation` resource that `/posts` (or `/deletes`) a `todo:item`.
Just like queries, mutations have an inputs-type-spec and outputs-type-spec. The inputs-type spec
has a foreign key field for every item-type that is posted (or deleted). This foreign key points
to an external type spec (e.g. `Todo`) whose fields (e.g. `id`, `name`, etc) are used as arguments
in the mutation. In case the mutation deletes an item, then only the item's id is used as an argument.
If the mutation posts or deletes multiple item types, then the mutation arguments are prefixed with the
type name, e.g. `todo_id` and `todolist_id`.

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
