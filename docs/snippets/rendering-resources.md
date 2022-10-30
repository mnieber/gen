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

@rule("module", has, "item")
def module_has_item(module, item):
    module.renders(
        [item],
        item.item_name,
        dict(item=item),
        [Path(__file__).parent / "templates"],
    )
```

## Fact

Here, we see how a step in rendering cascade is set up in `module_has_item`. When `module` is rendered into an output directory 'D', it will also render `item` in the `item.item_name` subdirectory of `D`. It extends the rendering context with `dict(item=item)` and renders the templates in the given template path.

## Fact

The jinja2 templates are found by looking for the "j2" extension. If the template is called `foo.bar.j2` then its content will be written to `foo.bar`.

## Snippet (`bar_pkg/item/templates/foo.bar.j2`)

```
Hello, my name is {{ item.item_name }}.
```

## Fact

As expected, you can use the variables that are defined in the Jinja2 context in the Jinja2 template.

## Snippet (`bar_pkg/item/templates/__moonleap__.j2`)

```
my-item.py.j2:
    name: {{ item.item_name }}.py
    include: {{ item.is_public|bool }}
```

## Fact

To choose a different output name, add a `__moonleap__.j2` file to the template directory. Moonleap will render this special template and use the result to look up two things: the output filename that should be used for a given template input-file, and the flag that tells Moonleap if the given input-template should be used at all.

## Fact

Sub-directories in the :template-directory are also created in the :output-directory. These sub-directories can have their own `__moonleap__.j2` file.

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
