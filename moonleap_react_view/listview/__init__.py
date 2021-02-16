import moonleap.resource.props as P
from moonleap import MemFun, Prop, extend, render_templates, rule, tags
from moonleap.utils.inflect import plural
from moonleap.verbs import has, shows
from moonleap_react.module import Module

from . import props
from .resources import ListView


@tags(["list-view"])
def create_list_view(term, block):
    plural_name = plural(term.data)
    list_view = ListView(
        item_name=term.data, name=f"{plural_name.title()}ListView", import_path=""
    )
    return list_view


@rule("module", has, "list-view")
def module_has_list_view(module, list_view):
    module.add_component(list_view)


@extend(ListView)
class ExtendListView:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "list-view")
    item_list = Prop(props.item_list)
