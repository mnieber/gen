import moonleap.resource.props as P
from moonleap import MemFun, Prop, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_react.module import Module

from .resources import ListView


@tags(["list-view"])
def create_list_view(term, block):
    name = term.data
    list_view = ListView(item_name=name, name=f"{name}ListView", import_path="")
    return list_view


@rule("module", has, "list-view")
def module_has_list_view(module, list_view):
    list_view.output_path = module.output_path
    module.service.add_tool(list_view)
    module.service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(ListView)
class ExtendListView:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "list-view")


@extend(Module)
class ExtendModule:
    list_views = P.children(has, "list-view")
