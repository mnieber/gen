How scopes are used to create resources
=======================================

Every block in a :spec-file can specify one or more scopes. Scopes are string values that identify the creation
and relation rules that should be used to: a) create the resources that are described in that block and b)
process the relations (between resources) that are declared in the block. The Moonleap settings file contains a mapping
from scopes to Python packages.
If a block title contains a link then the body of that block is replaced with the
contents of that link. In addition, the name of the linked file is added as a scope to the block.


Case 4: a :spec-file that illustrates scopes and links
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
3. For debugging purposes, the fully expanded :spec-file is written to the moonleap directory.
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
    def create_item(term):
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
    def create_module(term):
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
