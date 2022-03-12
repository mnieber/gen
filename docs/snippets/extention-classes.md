# :Extension-classes

## Snippet (`bar_pkg/item/__init__.py`)

```
from moonleap import extend, MemFun, Prop, MemField
from foo_pkg.bar import Bar, Baz

@extend(Item)
class ExtendItem:
    create_bar = MemFun(lambda self: Bar())
    baz = Prop(lambda self: Baz())
    foo = MemField(lambda: False)
```

## Fact

An :extension-class adds member functions to an already existing class. Here, we add a `create_bar` member-function to the `Item` class. This member-function receives a `self` argument (as all member-funtions do) and returns a `Bar` instance. We also added a `baz` property that returns a `Baz` instance. Finally, we added a `foo` field that stores a boolean value, which is initialized to `False`.

## Snippet (`bar_pkg/item/__init__.py`)

```
from moonleap import extend, MemFun

def meta():
    from foo_pkg.bar import Bar

    @extend(Item)
    class ExtendItem:
        create_bar = MemFun(lambda self: Bar())

    return [ExtendItem]
```

## Fact

Sometimes you can run into circular import problems when creating an :extension-class. In that case you can create a function called `meta` that has its own import statements and returns a list of :extension-classes. In this example, we extend `Item` with the same `create_bar` function that we saw earlier, but he import is moved inside a `meta` function.

## Snippet (`bar_pkg/module/__init__.py`)

```
import moonleap.resource.props as P
from moonleap import kebab_to_camel, create, extend, Prop, dataclass

from .resources import Module

@create("module")
def create_module(term):
    return Module(name=kebab_to_camel(term.data))

@extend(Module)
class ExtendModule:
    service = P.parent("service", owns)
    services = P.parent("service", uses)
    store = P.child(has, "store")
    components = P.children(has, "component")
```

## Fact

To render a resource, it's usually important to know its relations to other resources. Moonleap offers a number of standard properties - that you can use in class extensions - to give access to relations: `child`, `children`, `parent`, and `parents`. Here:

- the `service` property returns the parent `:service` resource that `/owns` this module,
- the `services` property returns all parent `:service` resources that `/uses` this module,
- the `store` property returns the child `:store` resource (where `:module /has :store`)
- the `components` property returns all child `:component` resources (where `:module /has :component`)

## Snippet (`bar_pkg/module/__init__.py`)

```
import moonleap.resource.props as P
from moonleap import kebab_to_camel, create, extend, Prop, dataclass

from .resources import Module

@create("module")
def create_module(term):
    return Module(name=kebab_to_camel(term.data))

@rule(["module", has, "component"])
def module_has_component(module, component):
    module.configs.add_source(component.configs)

@extend(Component)
class ExtendComponent:
    configs = P.tree("configs")

@extend(Module)
class ExtendModule:
    components = P.children(has, "component")
    configs = P.tree("configs")
    all_configs = Prop(lambda self: self.configs.merged)
```

## Fact

When you extend a class with `P.tree` then the class obtains a new property of type `Tree`. The `Tree` type has the following members:

- `add`: a function that adds an item to the tree
- `add_source`: a function that adds an item-source (also of type `Tree`) to the tree.
- `merged`: a function that returns a list of all items that were added to this `Tree` or any of its item-sources.

## Fact

In the example, we added a `configs` property to the `Component` resource class and to the `Module` resource class. Whenever we find out that a `module` has a `component` then we add `component.configs` as an item-source to `module.configs`. We also added a `all_configs` property that lists the config objects in the `Module` and all its related `Component` children (by calling `self.configs.merged`).
