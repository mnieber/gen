Glossary
========

**(spec) block**: a section of the spec file
**block body**: the text of the block section
**block scope**: a label that is added to a block to indicate which scope it belongs to (e.g. backend, frontend, database, etc). Every scope has associated creation rules and relation rules
**block title**: the heading of the block in the spec file
**creation rule**: a rule that turns a term into a resource
**external link**: a link to an external spec file that is included into the spec file
**moonleap dir**: an output directory where all results are written
**package**: a python package containing Moonleap rules and resources
**relation rule**: a rule that updates existing resources that are in a certain relationship
**scope**: a label - associated with a block - that determines which packages are used to process that block
**spec dir**: the directory that contains the spec file
**spec file**: the root markdown file that contains the project specification
**term**: a word in the spec that contains - or is prefixed by - a colon.
**term data (part)**: The part of the term before the colon.
**term name (part)**: The part of the term before the plus sign.
**term tag (part)**: The part of the term after the colon.
**verb**: a word in the spec that is prefixed with a forward slash

Purpose
=======

Moonleap turns a markdown-based spec file into a set of source files. There are four code generation steps:

1. Parse the spec file(s) to build a graph structure of (Python) resource objects that have
   relations to other resources.
2. Match every relation in the graph to a rule set, and run the matching rules. This step
   allows you to enrich the resources with additional information.
3. Render each resource into one or more source files.
4. Run post-processing steps such as code formatters.

Below, we will explain the process by introducing concepts and use-cases. Note that since Moonleap is a general
purpose rule-based code generator, it doesn't provide any specific rules that you could use to generate source code.
However, there is a companion package called Titan (one of the moons around Saturn) that is based on Moonleap,
which allows you to create a stack based on Docker, Django and React.


The spec dir
============

The spec file is called `spec.md` and it is located in the so-called spec dir. The purpose of the
spec file is to describe your project in a way that allows Moonleap
to generate source code for it. The spec file is written in markdown. It uses (annotated) natural
language, which also means that at times it will be ambiguous, and in those cases Moonleap will try to
make a reasonable choice. As we will see later, the generated code is treated as a shadow project,
from which useful parts are copied to your real project. This means that the shadow project
does not have to be perfect, as long as it is useful.


Spec files, terms and relations
===============================

The most important ingredients of the spec file are so-called terms and verbs. Terms are words
in the spec that follow a pattern of name+data:tag, e.g. `main+todo:list-view`. Moonleap will turn
every term into a (Python) `resource` object, that can be rendered into a set of source files.
Verbs are words that are prefixed with a slash, e.g. `/shows`. By connecting two terms with a verb,
you indicate a relation between resources, e.g. `the welcome:screen /shows the main+todo:list-view`.
The parser understands constructions such as "the backend:service and frontend:service /have a welcome:endpoint,
status:endpoint and about:endpoint that can be /called from the frontent:service". In this example, the /have
verb is involved in six relations, and /called in three relations. You can use parentheses
to limit the visibility of a term, e.g. "the (backend:service which /connects to :postgres) /has a welcome:endpoint".

The `name`, `data` and `tag` part
---------------------------------

Generally speaking, the `tag` part of a term indicates a resource type (`list-view`),
the data part indicates a flavour of that type (it's a `list-view` of `todo` elements) and the
`name` part indicates a named instance of this resource type (it's an instance of a `todo:list-view`
that is named `main`). The `name` part is optional, so you could specify that a
`todo:module /defines a todo:list-view` using only references to types (`todo:module` and
`todo:list-view`).

Blocks
======

To create resources for terms, Moonleap needs to know which terms in the spec file introduce a new
resource, and which terms are merely repeated. To solve this problem, the parser treats the spec file as a
collection of text blocks, where each block (title) corresponds to a Markdown section (title).
If a term appears in a block title, then we say that the block _describes_ that term. This means
that Moonleap will create a resource for that term using the specific resource creation rules
that are associated with the block. If the term is repeated in the block body (or in a child block) then
no new resource is created. We will later explain the exact rules that govern the resource creation process.

Case 1: a spec file describes resources and their relations
===========================================================

Description
-----------

Below we show a small (markdown) spec file.

The example (e.g.: specs/foo/spec.md)
-------------------------------------

.. code-block:: markdown

    # The foo:project [1]

    The foo:project /uses the bar:service and the baz:service [2].
    :It /shows a (welcome:screen that /has a :cookie-notice) that /uses the welcome:endpoint [3-5].

    ## The bar:service

    The bar:service has a simple goal:: it /provides the bar:endpoint. [6]

Notes
-----

1. Every section of the spec file defines a block. The section title defines the block title.
2. Since one resource is mentioned before the verb (/uses) and two after, there will be two relations created here.
3. The :it term refers to the first term in the previous sentence.
4. The :cookie-notice term has an data part that is the empty string ("").
5. Parentheses are used to limit the scope of the /has verb. Without these parentheses, it would (wrongly) state
   that the cookie-notice uses the welcome endpoint.
6. To use a colon in the spec file without identifying a resource, it needs to be doubled. This is why the word
   goal is proceeded by a double colon (::).


Creation and relation rules
===========================

A Moonleap (Python) module contains creation rules that convert terms into Python resource objects.
Every creation rule has an associated term-pattern that can be matched against a term. This pattern can include a name,
data and tag pert. The most specific creation rule that matches the term is used to create the resource for that term.
A module can also contains relation rules. A relation rule has an subject term-pattern, a verb and an object term-pattern.
For every relation between resources that the spec file describes, all matching relation rules are executed
in order to enrich the resources in that relation. A relation rule may return a list of additional
relations, which are processed in the same way as the relations in the spec file.


Term matching rules
===================


Case 2: a module contains creation rules and relation rules
===========================================================

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

    @rule("graphql:api", ("posts", "saves"), "item")  # [6,7]
    def graphql_api_posts_item(graphql_api, item):
        # Take any action here to enrich graphql_api and item.
        item.used_by_api = True
        # Return an additional relation that will be matched against the current set of rules
        return [
            create_forward(graphql_api, has, f"post-{item.item_name}:mutation"),   # [8,9]
            create_forward(graphql_api, documents, item),   # [10]
        ]

Notes
-----

1. The the filename, we can see that this Python module is part of the `bar_pkg` Moonleap (Python) package. As will be explained
   later, you can indicate in the settings file which moonleap packages must be used to process the spec file.
2. A new resource class is declared here.
3. The create decorator indicates a creation rule. The term-pattern for this creation rule only contains a tag part.
   The creation rule receives the term and the block that describes the term, and returns the resource object.
4. By convention, terms (in the spec file) use kebab case, which is converted here into camel case.
5. This creation rule is a more specific match for the `project:item` term. It will be called instead of the more
   general creation rule right above it.
6. A relation rule will be called by Moonleap for any relation in the spec file that matches the rule. A matching relation rule
   receives the matching resources as arguments.
7. Verbs in relation rules can be defined as tuples that contain different variants, so that it makes no difference
   whether you write /posts or /saves.
8. A relation rule may return a new list of relations that are processed in the same way as the relations
   from the spec file. If needed, new resources (mentioned in these relations) will be created.
9. The create_forward helper function will accept arguments that are either a term or a resource. In the
   latter case, it converts the resource into a term (Moonleap remembers which term was used to create the resource).
10. Note that a resource may be twice related to another resource (using different verbs, in this case
   "posts" and "documents").


The rules that govern resource creation
=======================================

There are special rules that determine which blocks describe which terms. Moonleap uses this information to
determine if a term introduces a new resource, and to determine which creation rules must be used to
create it.

In general, the question we must answer is: if a blocks mentions a term, then which block is describing that term?
To answer this question we use the notion of "competing blocks". For any block, it's competing blocks are:
- the block itself
- all its (grand)child blocks
- all its (grand)parent blocks
- all direct children of its (grand)parent blocks

The answer to our question is:
1. if a competing block mentions the term it its title, then this block describes the term. If more than 1 such
   block can be found then it's considered an error. If no such block is found, then rule 2 (below) is used
2. the competing (grand)parent block that mentions the term and is highest in the tree describes the term

The sloppy (but convenient) way to use these rules is to say that:
- the block that mentions the term in its title describes it
- otherwise, the parent block is the one describing the term (the child block references it)
- the concept of parent/child is bent a little so that also "the direct child of my (grand)parent can be
  considered my (grand)parent" but we only use this bent concept if that "grand-parent" mentions the term in
  its title. The mental picture here is that a child block's title explains some detail about its parent block.

We can now ask in which cases a term that appears in two blocks (B1 and B2) refers to the same resource in
both blocks. One required condition is that B1 and B2 are competing (B1 is a competing block for B2,
or vice versa). But this is not a sufficient condition. Consider the case where B1 is a competing block for B2,
but B1 and B2 are not related by parent/child relations. In this case (without loss of generality) assume that
the parent of B1 is a (grand)parent of B2. In this case, if B1 mentions the term in its title, then the term refers
to the same resource in both blocks, but otherwise, it doesn't.

There is one additional rule to explain, which has to do with wildcards: if a block title contains a term such as
x:service or profile:x, then it describes any terms - appearing in the block body - that match this wildcard
(e.g. account:service, or profile:screen). If a parent block mentions foo:x in their title, and a child block
mentions x:bar, then the term foo:bar is considered to be described by the parent block (this case is not an error).


Case 3: a spec file that illustrates resource creation
======================================================

The example (e.g.: specs/foo/spec.md)
-------------------------------------

.. code-block:: markdown

    # The foo:project [1]
    The foo:project uses the bar:service and the baz:service. It /shows the welcome:screen.

    ## The bar:service [2]
    The bar:service /has a welcome:endpoint that is /used in the welcome:screen.

    ### Details
    The welcome:screen also /shows a baz:banner. [3]

    ## The baz:x [4]
    The baz:service /has a welcome:endpoint. :It /shows the baz:banner.

Notes
-----

1. In this example, there are four blocks. The first block describes foo:project and welcome:screen, but
   (based on rule 1) not bar:service and not (based on rule 3) baz:service.
2. This block describes bar:service and welcome:endpoint. It references welcome:screen.
3. This block references baz:banner (because the last block is a competing block that mentions baz:banner in
   its title via the baz:x wildcard)
4. This block describes (via the rule about wildcards) baz:service and welcome:endpoint. The welcome:endpoint terms
   in the "bar:service" block and "baz:x" block are unrelated. That would change if the  were
   a child of the "bar:service" block, or if the "baz:x" block would mention "welcome:screen" in its title.


How scopes are used to create resources
=======================================

Every block in a spec file can specify one or more scopes. Scopes are string values that identify the creation
and relation rules that should be used to: a) create the resources that are described in that block and b)
process the relations (between resources) that are declared in the block. The Moonleap settings file contains a mapping
from scopes to Python packages.
If a block title contains a link then the body of that block is replaced with the
contents of that link. In addition, the name of the linked file is added as a scope to the block.


Case 4: a spec file that illustrates scopes and links
=====================================================

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

    packages_by_scope:  # [5]
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

    modules = [  # [6]
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
5. This key in the settings file describes which Moonleap packages are used per scope.
6. Every moonleap package has an init file that lists the module that should be loaded for that package.


Extension classes
=================

If a resource object has a render function, then Moonleap will call it so that code is generated for
that resource.  Moonleap gives a lot of options to users to influence how code is generated. Therefore,
resource objects typically do not have a hard coded render function. Instead, the render function
(of your choice) is added dynamically to the resource class using the `@extend` decorator.
The default implementation of `render` will iterate over all jinja2 templates in the resource's
template directories, and render each template using `res` as the variable that contains
the resource. The jinja2 templates are found by looking for the "j2" extension. If the template
is called `foo.bar.j2` then its content will be written to `foo.bar`. To choose a different
output name, add a `foo.bar.fn` template: Moonleap will render this "fn" template and use the
output as the filename that should be used instead of `foo.bar` (the default output filename). It's also possible
to put a jinja2 tag directly in the template name, e.g. `{{ res.name }}.txt.j2`.
Note that directories that appear in the template directory are also created in the output directory.
They too can have names with jinja2 tags, and associated ".fn" files.

Accessing relations
-------------------

To render a resource, it's usually important to know its relations to other resources.
Moonleap offers four standard properties - that you can use in class extensions - to give
access to relations: `child`, `children`, `parent` and `tree`. The `tree` property allows
you to recursively collect resources that are "relatives of relatives".


Case 5: a Moonleap module that uses an extension class
======================================================

The example
-----------

.. code-block:: python

    # bar_pkg/item/__init__.py

    from moonleap import kebab_to_camel, create, Resource, MemFun
    from dataclasses import dataclass

    @dataclass
    class Item(Resource):
        item_name: str

    def get_context(item_resource):
        return dict(res=item_resource)

    @create("item")
    def create_item(term, block):
        item = Item(
            item_name=kebab_to_camel(term.data)
        )
        item.add_template_dir(Path(__file__).parent / "templates", get_context)  # [1]

    @extend(Item)
    class ExtendItem(StoreTemplateDirs):  # [2]
        # The render function is supplied by the StoreTemplateDirs base class
        pass

    # Alternatively, you can use the special meta() function, which allows you
    # to do additional imports which would otherwise create a circular import dependency.

    if False:  # we are not actually using the meta function here
        def custom_render(self, write_file, render_template, output_path):  # [3]
            template_path = Path(__file__).parent / "templates"
            render_templates(template_path)(self, write_file, render_template, output_path)

        def meta():
            from foo_pkg.bar import Bar

            @extend(Item)
            class ExtendItem:
                render = MemFun(custom_render)  # [4]
                create_bar = MemFun(lambda self: Bar())

            return [ExtendItem]

Notes
-----

1. This is the typical way to render a directory with jinja2 templates with a jinja2 context that
   contains the resource. Note that the `res` key is added automatically to the context, so
   you could leave out `res=item_resource` in `get_context` (or you could leave out the `get_context`
   argument entirely).
2. The `StoreTemplateDirs` class is a mixin that adds the `add_template_dir` method to the resource class.
   It also adds a `render` function that renders all templates added with `add_template_dir`.
3. This is an example of a custom render function (in this case, `StoreTemplateDirs]` is not used).
4. `MemFun` is a helper function adds a special tag to a stand-alone function. This tag lets Moonleap
   know that this stand-alone function must be added as a member function to the extended class.


Case 6: an extension class that offers access to relations
==========================================================

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
        module_configs = P.tree("module_configs")  # [5]
        merged_config = Prop(lambda self: self.configs.merged)  # [6]

    @extend(Component)
    class ExtendComponent:
        module_configs = P.tree("module_configs")

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
