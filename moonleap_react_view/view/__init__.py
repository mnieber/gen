import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Rel,
    add,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    word_to_term,
)
from moonleap.verbs import has
from moonleap_react.module import Module

from .resources import View


@tags(["view"])
def create_view(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    view = View(name=name, kebab_name=kebab_name)
    return view


@rule("module", has, "view")
def module_has_view(module, view):
    view.output_path = module.output_path
    module.service.add_tool(view)


@extend(View)
class ExtendView:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "view")


@extend(Module)
class ExtendModule:
    views = P.children(has, "view")
