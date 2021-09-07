The code generation steps
=========================

There are five steps to the code generation:

1. Parse the spec files to build a graph structure of resources (the nodes) and
   verbs (the edges)
2. Create a resource object for every node in the graph (also using the edges)
3. Match every relation in the graph to a rule set, and run the matching rules.
4. Render each resource into one or more source files.
5. Run post-processing steps such as code formatters.

The parsing step
----------------

Blocks
~~~~~~

The spec file is called `spec.md` and lives in its own spec directory,
together with a `settings.yml` file. The format of the spec file is Markdown.
The parser treats the spec file as a collection of text blocks,
where each block (title) corresponds to a Markdown section (title).

Terms, verbs and relations
~~~~~~~~~~~~~~~~~~~~~~~~~~

The parser scans the text block for nouns (words that contain a colon, such as :project and backend:service)
and verbs (prefixed with a slash, such as /uses).
For every noun, it creates a Term object that is added as a node to the graph, and for every verb it adds a
Rel object (short for Relation) that is added as an edge. Terms have a tag part (everything after the colon)
and a data part (everything before). For example, the backend:service term has "service" as the tag part and
"backend" as the data part.
The parser understands constructions such as "the backend:service and frontend:service /have a welcome:endpoint,
status:endpoint and about:endpoint that can be /called from the frontent:service". In this example, the /have
verb is involved in six relations, and /called in three relations. You can use parentheses
to limit the visibility of a term, e.g. "the (backend:service which /connects to :postgres) /has a welcome:endpoint".
Note that verbs can be defined as tuples that contain different variants, such as
("has", "have"), so that it makes no difference whether you write /has or /have.


Finding out where terms are described
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a term such as submit:button is used in different blocks, it's important to know if these blocks are in fact
referring to the same button, or to distinct ones. The parser follows some simple rules to determine this. To
avoid surprises, it's essential that you understand these rules (note that the words 'parent' and 'child' used
below are meant to also include grand-children and grand-parents).

The first rule applies when a term is mentioned in a block title:

1.0 if a block B mentions a term in its title, then we say that it _describes_ that term.
1.1 if B's parent or child block also mentions the term in its body, then then we say that it _references_ that term.
1.2 if a parent and child block describe the same term (they both mention it in their title) then
it's considered an error

The second rule applies when a child block repeats a term that appears in the body of a parent block. It deals with cases
that are not handled by the first rule (which focusses on the block title)

2.0 if a block mentions a term in its body, and a child block also mentions it, then we say that the parent block
    _describes_ the term and the child block _references_ it.

The third rule is about wild-cards.

3.0 If a block title contains a term such as x:service or profile:x, then it
describes any terms that match this wildcard (e.g. account:service, or profile:screen).
3.1 If a parent block mentions foo:x in their title, and a child block mentions x:bar, then the term foo:bar is
considered to be described by the parent block (this case is not an error).


An example spec
~~~~~~~~~~~~~~~

Consider the following spec:

.. code-block:: bash

    # The foo:project
    The foo:project uses the bar:service and the baz:service. It /shows the welcome:screen.

    ## The bar:service
    The bar:service /has a welcome:endpoint that is /used in the welcome:screen.

    ## The baz:x
    The baz:service /has a welcome:endpoint.

In this example, there are three blocks. Let's call them Foo, Bar and Baz. The
Foo block describes foo:project and welcome:screen, but (based on rule 1) not bar:service and not
(based on rule 3) baz:service.
The Bar block describes bar:service and welcome:endpoint. It references welcome:screen.
The Baz block describes baz:service and welcome:endpoint. The welcome:endpoint terms
in Bar and Baz are unrelated. The situation would change if Baz were a child of Bar,
because in that case it would be referencing the welcome:endpoint of Bar.

Links
~~~~~

By using links, it's possible to move part of the spec to a different file:

.. code-block:: bash

    # The foo:project
    The foo:project uses the bar:service and the baz:service.

    ## The [bar:service](./bar-service.md)

    ## The [baz:service](./baz-service.md)

When you put a link into the block title, you should leave the body empty.
The parser will read the included file and insert it as the body of the text block.

Scopes
~~~~~~

We need to discuss one more topic related to parsing: scopes. Scopes are labels that can
be attached to a text block. The resource building step can use these labels to produce
the right resources for the terms that the block describes. For example, we could have
a Backend, Cloud and Frontend scope:

.. code-block:: bash

    # The foo:project
    The foo:project uses the bar:service and the baz:service.

    ## The bar:service {Backend, Cloud}
    The bar:service /has a welcome:endpoint.

    ## The baz:service {Frontend}
    The baz:service /has a welcome:endpoint.

Every link (see above) automatically defines a scope. This means that if a block
includes the bar-service.md file then all its child blocks (and the block itself)
will have the `bar-service` scope.

The resource creation step
--------------------------

The resource creator converts every term into a resource, using the following steps:

- it determines which block describes the resource, and the scopes associated with that block
- it loads the rules for these scopes (all rules are plain functions)
- it find the best matching (i.e. the most specific) "create" rule and calls it to create the
  resource
- for every relation that the resource has to other resources (the edges in the graph), the resource
  creator executes the "relation" rules that match this relation. These "relation" rules allow you to
  enrich the resource objects. Relation rules can return follow-up rules that are also executed.


How to select rules for each scope
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can associate rules with a scope by setting the packages_by_scope key of the `settings.yml`
file (that is located next to the `spec.md` file). Note that the default scope is associated
with every block:

.. code-block:: yaml

    packages_by_scope:
    default:
        - titan.dodo_pkg
        - titan.project_pkg

Every package exports a variable called `modules`. Each module in this list can contain creation
rules and relation rules. A create rule is decorated with `@create`. It receives a list of tags
to match against, and returns a resource object:

.. code-block:: python

    from .resources import Item

    @create("item")
    def create_item(term, block):
        assert term.tag == "item"
        return Item(item_name=term.data)

A relation rule is decorated with `@rule`. It receives a subject term, a verb and an object term.
It optionally returns a Forward object (or list thereof) that contains additional relations.

.. code-block:: python

    @rule("graphql:api", posts, "item")
    def graphql_api_posts_item(graphql_api, item):
        # Take any action here to enrich graphql_api and item.
        pass
        # Return an additional relation that will be matched against the current set of rules
        return [create_forward(graphql_api, has, f"post-{item.item_name}:mutation")]


An example package
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from . import graphqlapi, item, itemlist, itemtype, mutation, query

    modules = [
        graphqlapi,
        item,
        itemlist,
        itemtype,
        mutation,
        query,
    ]

An example module
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from moonleap import kebab_to_camel, kebab_to_snake, create, Resource
    from .resources import Item
    from dataclasses import dataclass

    @dataclass
    class Item(Resource):
        item_name: str
        item_name_snake: str

    @create("item")
    def create_item(term, block):
        return Item(
            item_name=kebab_to_camel(term.data),
            item_name_snake=kebab_to_snake(term.data),
        )

    @rule("graphql:api", posts, "item")
    def graphql_api_posts_item(graphql_api, item):
        pass  # Take any action here to enrich graphql_api and item

