import os

import moonleap.resource.props as P
from moonleap import MemFun, Prop, extend, render_templates, rule, tags
from moonleap.render.template_env import add_filter
from moonleap.utils import title
from moonleap.utils.inflect import plural
from moonleap.verbs import has
from moonleap_react.module import Module

from . import props
from .resources import ListView


@tags(["list-view"])
def create_list_view(term, block):
    plural_name = plural(term.data)
    list_view = ListView(
        item_name=term.data, name=f"{title(plural_name)}ListView", import_path=""
    )
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
    item_list = Prop(props.item_list)


@extend(Module)
class ExtendModule:
    views = P.tree(has, "list-view")


add_filter("store", lambda x: plural(x) + "Store")
add_filter("byId", lambda x: x + "ById")
add_filter("plural", lambda x: plural(x))
add_filter("untitle", lambda x: x[0].lower() + x[1:])
add_filter("expand_vars", lambda x: os.path.expandvars(x))
