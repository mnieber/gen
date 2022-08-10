# :Resources

## Snippet (`bar_pkg/item/__init__.py`)

```
from moonleap import kebab_to_camel, create, extend, Path
from .resources import Item

def get_context(item_resource):
    return dict(res=item_resource)

@create("item")
def create_item(term):
    item = Item(item_name=kebab_to_camel(term.data))
    item.add_template_dir(Path(__file__).parent / "templates", get_context)

@extend(Item)
class ExtendItem(StoreTemplateDirs):
    pass
```

## Fact

If a :resource has a render function, then Moonleap will call it so that code is generated for
that :resource. Here, the render function is added dynamically using the `StoreTemplateDirs` :extension-class. This :extension-class also adds the `add_template_dir` function.

## Fact

The `add_template_dir` function takes two arguments: a :template-directory and a `get_context` function. The `get_context` function takes the resource as it's argument, and returns a Jinja2 context. Here, the `item_resource` :resource is stored under the `res` key (note that this is a Moonleap convention).

## Fact

For each :template-directory and corresponding `get_context` function that were added with `add_template_dir`, the `render` function creates a Jinja2 context (using `get_context`) and uses it to render all Jinja2 templates in the given templates directory.

## Fact

The jinja2 templates are found by looking for the "j2" extension. If the template is called `foo.bar.j2` then its content will be written to `foo.bar`.

## Snippet (`bar_pkg/item/templates/foo.bar.j2`)

```
Hello, my name is {{ res.name }}.
```

## Fact

As expected, you can use the variables that are defined in the Jinja2 context in the Jinja2 template.

## Snippet (`bar_pkg/item/templates/foo.bar.j2.fn`)

```
{{ res.name }}.txt
```

## Fact

To choose a different output name, add a `foo.bar.j2.fn` template: Moonleap will render this "fn" template and use the output as the filename that should be used instead of `foo.bar` (the default output filename). Here, the output filename will have the `.txt` extension and a name that is based on the name of the resource.

## Fact

It's also possible to put a jinja2 tag directly in the template name, e.g. `{{ res.name }}.txt.j2`.

## Snippet (`bar_pkg/item/templates/hello/foo.bar.j2`)

```
Hello, my name is {{ res.name }}.
```

## Fact

Directories that appear in the :template-directory are also created in the :output-directory. They too can have names with jinja2 tags, and associated ".fn" files. Here, the output filename for the `hello/foo.bar.j2`) is `hello/foo.bar`.

## Snippet

```
def custom_render(self, write_file, render_template, output_path):
    template_path = Path(__file__).parent / "templates"
    render_templates(template_path, self, write_file, render_template, output_path)

@extend(Item)
class ExtendItem:
    render = MemFun(custom_render)
```

## Fact

A :render-function takes the following arguments:

- write_file: a function that takes an `output_filename` argument and a `content` argument and writes the given `context` to the given `output_filename`.

- render_template: a function that takes a Jinja2 template filename and a context (as a list of named arguments) and returns an output content

- output_path: a filename where the output of render_template should be stored (using `write_file`)

## Fact

Here, we show how the standard `render_templates` function is used to render all templates in `template_path` using the given `write_file`, `render_template` and `output_path` arguments. Note that `ExtendItem` is an :extension-class.

## Snippet (`bar_pkg/module/__init__.py`)

```python
filters = {
    "expand_vars": lambda x: os.path.expandvars(x)
}
```

## Fact

A module may have a `filters` variable that contains a list of jinja2 filters. These filters become available in all templates (in other words, not limited to particular :scopes).

## Snippet (`bar_pkg/module/__init__.py`)

```python
transforms = [
    process_clean_up_py_imports
]
post_transforms = [
    post_process_clean_up_py_imports
]
```

## Fact

A module may declare a `transforms` variable that contains a list of :transforms that are applied
to each template before it is passed to jinja2, and a list of `post_transforms` that are applied
to the output of each template.
