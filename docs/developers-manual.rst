Glossary
========

**(spec) block**: a section of the spec file
**block body**: the text of the block section
**block scope**: a label that is added to a block to indicate which scope it belongs to (e.g. backend, frontend, database, etc). Every scope has associated creation rules and relation rules
**block title**: the heading of the block in the spec file
**creation rule**: a rule that turns a term into a resource
**external link**: a link to an external spec file that is included into
the spec file
**moonleap dir**: an output directory where all results are written
**package**: a python package containing Moonleap rules and resources
**relation rule**: a rule that updates existing resources that are in a certain relationship
**scope**: a label - associated with a block - that determines which packages are used to process that block
**spec dir**: the directory that contains the spec file
**spec file**: the root markdown file that contains the project specification
**term**: a word in the spec that contains - or is prefixed by - a colon.
**term data**: The part of the term before the colon.
**term tag**: The part of the term after then colon.
**verb**: a word in the spec that is prefixed with a forward slash

Purpose
=======

Moonleap turns a markdown-based spec file into a set of source files.
Below, the process will be explained using annotated use-cases.

Case 1: a spec file describes resources and their relations
===========================================================

Description
-----------

Moonleap processes a spec file written in markdown. This spec file contains blocks (which correspond
to markdown sections) that contain terms (words that have a colon in them) and verbs (words that start with a slash).
These terms and verbs will later be translated into resources and relations (according to block specific rules),
which are then rendered using jinja2 templates.

The example (file: specs/foo/spec.md)
-------------------------------------

.. code-block:: markdown

    # The foo:project [1-2]

    The foo:project /uses the bar:service and the baz:service [3-4].
    :It [4] /shows a (welcome:screen that /has a :cookie-notice) that /uses the welcome:endpoint [5].

    ## The bar:service [6-7]

    The bar:service has a simple goal:: it /provides the bar:endpoint. [8]

Notes
-----

1. Every section of the spec file defines a block. The section title defines the block title.
2. A word with a colon in it is called a term. It identifies a resource. The part of the term before the colon
   is called 'data' and the part after the colon is called 'tag'. The tag and data parts are used as inputs
   for the (resource) create rules.
3. A word that starts with a slash is called a verb. It establishes a relationship between resources.
   Moonleap has so-called relation rules and a rule-matching engine that are used to enrich resources based on
   their relations to other resources.
4. Since one resource is mentioned before the verb (/uses) and two after, there will be two relations created here.
5. The :it term refers to the first term in the previous sentence.
6. Parentheses are used to limit the scope of the /has verb. Without these parentheses, it would state
   that the cookie-notice uses the welcome endpoint (that would be wrong).
7. If a term appears in a block title, then we say that the block _describes_ that term. For every term, there is
   exactly one block that describes that term. It's important to know which blocks describe which terms, because -
   as will be explained later - every block has an associated set of create and relation rules.
8. To use a colon in the spec file without identifying a resource, it needs to be doubled. This is why the word
   goal is proceeded by a double colon (::).


Case 2: a module contains create rules and relation rules
=========================================================

Description
-----------

A Moonleap (Python) module contains create rules that convert terms into Python resource objects.
The most specific create rule that matches a term is called to create the resource for that term.
The module also contains relation rules. For every relation, all matching relation rules are called
to enrich the resources in that relation. A relation rule may return a list of additional relations,
which are processed in the same way.

The example
-----------

.. code-block:: python

    # bar_pkg/item/__init__.py  [1]

    from moonleap import kebab_to_camel, create, Resource
    from dataclasses import dataclass

    @dataclass
    class Item(Resource):  # [2]
        item_name: str

    @create("item")  # [3]
    def create_item(term, block):
        return Item(
            item_name=kebab_to_camel(term.data)  # [4]
        )

    @create("project:item")  # [5]
    def create_item(term, block):
        return Item(
            item_name="project",
        )

    @rule("graphql:api", posts, "item")  # [6]
    def graphql_api_posts_item(graphql_api, item):
        # Take any action here to enrich graphql_api and item.
        item.used_by_api = True
        # Return an additional relation that will be matched against the current set of rules
        return [
            create_forward(graphql_api, has, f"post-{item.item_name}:mutation"),   # [7]
            create_forward(graphql_api, uses, f":item", obj_res=item),   # [8-9]
        ]

Notes
-----

1. As will be explained later, Moonleap uses a settings file to configure which Python packages and modules
   are used for processing the spec file.
2. A new resource class is declared here.
3. The create decorator indicates a create rule. The create rule receives the term and the block
   that describes the term, and returns the resource object.
4. By convention, terms use kebab case, which is converted here into camel case.
5. This create rule is a more specific match for the `project:item` term. It will be called instead of the more
   general create rule right above it.
6. A relation rule will be called by Moonleap for any relation in the spec file that matches the rule.
7. A relation rule may return a Forward object (or list thereof) that contains additional relations.
   If needed, new resources will be created for this new relation.
8. When returning a new relation, you may use the `obj_res` field to specify the object in that
   relation (without this argument, Moonleap will find or create the object based on the ":item" term)
9. Note that the graphql_api resource is twice related to the item resource, using the "posts" and the
   "has" verbs.


Case 3: terms in a spec file are described by blocks
====================================================

Description
-----------

The following rules are used to determine which blocks describe which terms

1.0 if a block B mentions a term in its title, then we say that it _describes_ that term.
1.1 if B's parent or child block also mentions the term in its body, then then we say that it _references_ that term.
1.2 if a parent and child block describe the same term (they both mention it in their title) then
it's considered an error
2.0 if a block mentions a term in its body, and a child block also mentions it, then we say that the parent block
    _describes_ the term and the child block _references_ it.
3.0 If a block title contains a term such as x:service or profile:x, then it describes any terms - appearing in the
    block body - that match this wildcard (e.g. account:service, or profile:screen).
3.1 If a parent block mentions foo:x in their title, and a child block mentions x:bar, then the term foo:bar is
considered to be described by the parent block (this case is not an error).

The example (file: specs/foo/spec.md)
-------------------------------------

.. code-block:: markdown

    # The foo:project [1]
    The foo:project uses the bar:service and the baz:service. It /shows the welcome:screen.

    ## The bar:service [2]
    The bar:service /has a welcome:endpoint that is /used in the welcome:screen.

    ## The baz:x [3]
    The baz:service /has a welcome:endpoint.

Notes
-----

1. In this example, there are three blocks. The first block describes foo:project and welcome:screen, but
   (based on rule 1) not bar:service and not (based on rule 3) baz:service.
2. This block describes bar:service and welcome:endpoint. It references welcome:screen.
3. This block describes (based on rule 3) baz:service and welcome:endpoint. The welcome:endpoint terms in the
   "bar:service" block and "baz:x" block are unrelated. The situation would change if the "baz:x" block were a child
   of the "bar:service" block, because in that case it would be referencing the welcome:endpoint of
   that block (rule 2).


Case 4: blocks (in a spec file) have scopes and links
=====================================================

Description
-----------

Every block in a spec file can specify one or more scopes. Scopes are string values that identify the create
and relation rules that should be used to process the resources that are described in that block (and the relations
that this resource has to other relations). The Moonleap settings file contains a mapping from scopes to Python
packages. If a block title contains a link then the body of that block is replaced with the contents of that link.
In addition, the name of the linked file is added as a scope to the block.


The example (file: specs/foo/spec.md)
-------------------------------------

.. code-block:: markdown

    # The foo:project {foo, foobar}  [1]

    The foo:project uses the bar:service and the baz:service.

    ## The [bar:service](./bar-service.md)  [2,3]

    This body will be replaced (it could have been left empty, as in the next block below)

    ## The [baz:x](./baz-service.md)  [4]

.. code-block:: yaml

    # specs/foo/settings.yml

    packages_by_scope:
        default:
            - default_pkg
            - titan.project_pkg
        bar-service:
            - bar_pkg
        baz-service: []
        foo: []
        foobar: []

.. code-block:: python

    # bar_pkg/__init__.pyu

    from . import graphqlapi, mutation, query

    modules = [
        graphqlapi,
        item,
        itemlist,
    ]


Notes
-----

1. Every block automatically has the `default` scope.
   This block therefore has the `foo`, `foobar` and `default` scope. It will be processed using the
   rules in the `default_pkg` and `titan.project_pkg`.
2. This block has the `default` and `bar-service` scope. It will be processed using the
   rules in the `default_pkg`, `titan.project_pkg` and `bar_pkg`.
3. For debugging purposes, the fully expanded spec file is written to the moonleap directory.
4. This block has the `default` and `baz-service` scope. It will be processed using the
   rules in the `default_pkg` and `titan.project_pkg`.


Case 5: an extension class defines the resource.render function
===============================================================

Description
-----------

If a resource object has a render function, then Moonleap will call it so that code is generated for
that resource.  Moonleap gives a lot of options to users to influence how code is generated. Therefore,
resource objects typically do not have a hard coded render function. Instead, the render function
(of your choice) is added dynamically to the resource class using the `@extend` decorator.
The default implementation of `render` will iterate over all jinja2 templates in the resource's
template directory, and render each template using `res` as the variable that contains
the resource. The jinja2 templates are found by looking for the "j2" extension. If the template
is called `foo.bar.j2` then its content will be written to `foo.bar`. To choose a different
output name, add a `foo.bar.fn` template: Moonleap will render this "fn" template and use the
output instead of `foo.bar` (the default output filename). It's also possible to put a jinja2
tag directly in the template name, e.g. `{{ res.name }}.txt.j2`.
Note that directories that appear in the template directory are also created in the output directory.
They too can have names with jinja2 tags, and associated ".fn" files.

The example
-----------

.. code-block:: python

    # bar_pkg/item/__init__.py

    from moonleap import kebab_to_camel, create, Resource, MemFun
    from dataclasses import dataclass

    @dataclass
    class Item(Resource):
        item_name: str

    @create("item")
    def create_item(term, block):
        return Item(
            item_name=kebab_to_camel(term.data)
        )

    def render(self, write_file, render_template, output_path):
        template_path = Path(__file__).parent / "templates"
        render_templates(template_path)(self, write_file, render_template, output_path)

    @extend(Item)
    class ExtendItem:
        render = MemFun(render)  # [1]

    # Below, we show some alternatives for adding the render function
    #
    # @extend(Item)
    # class ExtendItem:
    #     render = MemFun(render_templates(Path(__file__).parent / "templates"))
    #
    # @extend(Item)
    # class ExtendItem(StoreTemplateDirs):
    #     # The render function is supplied by the StoreTemplateDirs base class
    #     # Call item.add_template_dir(Path(__file__).parent / "templates") to add a directory
    #     # to the list of directories that are searched for templates.
    #     pass
    #
    # Alternatively, you can use the special meta() function, which allows you
    # to do additional imports which would otherwise create a circular import dependency.
    #
    # def meta():
    #     from foo_pkg.bar import Bar
    #
    #     @extend(Item)
    #     class ExtendItem:
    #         render = MemFun(props.render)
    #         create_bar = MemFun(lambda self: Bar())
    #
    #     return [ExtendItem]

Notes
-----

1. `MemFun` is a helper function adds a special tag to a stand-alone function. This tag lets Moonleap
   know that this stand-alone function must be added as a member function to the extended class.


Case 6: an extension class offers access to the relations of a resource
=======================================================================

Description
-----------

To render a resource, it's usually important to know its relations to other resources.
Moonleap offers four standard properties (that you can use in class extensions) to give
access to relations: `child`, `children`, `parent` and `tree`. The `tree` property allows
you to recursively collect resources that are "relatives of relatives".

The example
-----------

.. code-block:: python

    # bar_pkg/module/__init__.py

    import moonleap.resource.props as P
    from moonleap import kebab_to_camel, create, Resource, Prop
    from dataclasses import dataclass
    from bar_pkg.component import Component
    from . import props

    @dataclass
    class Module(Resource):
        name: str

    @create("module")
    def create_module(term, block):
        return Module(
            name=kebab_to_camel(term.data)
        )

    @rule(["module", has, "component"])
    def module_has_component(module, component):
        module.configs.add_source(component.configs)  # [1]

    @extend(Module)
    class ExtendModule:
        service = P.parent(Service, has)  # [2]
        store = P.child(has, "store")  # [3]
        components = P.children(has, "component")  # [4]
        configs = P.tree(has, "module-config")  # [5]
        merged_config = Prop(lambda self: self.configs.merged)  # [6]

    @extend(Component)
    class ExtendComponent:
        configs = P.tree(has, "module-config")

Notes
-----

1. Because `module.configs` and `component.configs` are `tree` properties, we can connect them
   such that `component.configs` is included in the output of `module.configs.merged`.
2. This property finds the Service object that is in a "/has :module" relation with the module.
3. This property finds the Store object that the module is in a "/has :store" relation with.
4. This property finds the Component objects that the module is in a "/has :component" relation with.
5. This property finds the resources that the module is in a "/has :module-config" relation with. It
   potentially includes "relatives of relatives" using the `add_source` function described above.
6. A `tree` property has a member called `merged` that returns the flat list of all related resources
   (including "relatives of relatives").


Case 7: Modules can register jinja2 filters. Rendered output files can be post-processed.
=========================================================================================

Description
-----------

A module may declare a `transforms` variable that contains a list of transforms that are applied
to the template before it is passed to jinja2, and a list of `post_transforms` that are applied
to the output produced by jinja2. Furthermore, a module may have a `filters` variable that contains
a list of jinja2 filters. Finally, the moonleap settings file may contain a list of post-processing
steps.

The example
-----------

.. code-block:: python

    # bar_pkg/module/__init__.py

    filters = {"expand_vars": lambda x: os.path.expandvars(x)}

    # check the file default_pkg/clean_up_py_imports/transform.py for details
    transforms = [process_clean_up_py_imports]
    post_transforms = [post_process_clean_up_py_imports]

.. code-block:: yaml

    # specs/foo/settings.yml

    bin:
        prettier:
            exe: ~/.yarn/bin/prettier
            config: ~/.prettierrc
    post_process:
        '.ts(x)?': [prettier]
