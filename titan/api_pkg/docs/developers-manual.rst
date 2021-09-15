Purpose
=======

The api_pkg allows you to specify the data-model that is used by the various services
in your project, as well as the queries and mutations that work against this data-model.
Below, the process will be explained using annotated use-cases.

Case 1: a spec file describes item-types, items and item-lists
==============================================================

Description
-----------

The spec file can declare resources that represent item-types, items, and item lists. The
`foo:item` resource represents a single instance of the `foo:item-type`, whereas the
`foo:item-list` resource represents a list of `foo:item-type`.
The spec file can declare that a module stores an item-list. This means that the mentioned module
will define the data-model for that item.
By default, an item-type has a name and id field. However, you can add a JSON schema definition for
the item-type in the data-types directory. The fields in the JSON schema can be scalars, or foreign
keys to other data types.

The example
-----------

.. code-block:: python

    # generated file backend/foobars

    class FooBar(Model):
        id = models.Charfield(max_length=255)
        name = models.CharField(max_length=255)


Case 2: a spec file describes queries and mutations
===================================================

Description
-----------

The spec file can declare a `query` resource that provides (or posts, or deletes) a `foo:item` and/or
`bar:item-list`. Moonleap uses this information to decide which query to run when (for example) there
is a foo:list-view with delete:behaviour. Every query has an input data type (stored in the data-types
directory) that contains the inputs for that query, and an output data type. The output data type can
have fields of type "list".
If a query does not have an input data type (in the data-types directory) then it uses a default input
data type that has:
- an id-field if the query provides an item, or
- no fields if it provides an item-list.

The example
-----------

.. code-block:: python

    # generated file backend/api/query/foobarquery

    class FooBarQuery(Model):
        foo_bars = graphene.List(FooBarType, baz=graphene.Field(graphene.Integer))

        def resolve_foo_bars(self, info, baz: int):
            return FooBar.objects.filter()  # todo: use baz


.. code-block:: python

    # generated file backend/api/mutation/postfoobar

    class FooBarQuery(Model):
        class Arguments:
            baz = graphene.Field(graphene.Integer)

        ok = graphene.Boolean()
        errors = graphene.Any()

        def mutate(self, info, baz: int):
            x = FooBar(baz=baz)
            x.save()
            return FooBarQuery(
                ok=True,
                errors=[]
            )


Case 3: a spec file describes item-types, items and item-lists
==============================================================

Description
-----------

