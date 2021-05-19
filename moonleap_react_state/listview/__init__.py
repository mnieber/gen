from moonleap import MemFun, extend, kebab_to_camel, render_templates, tags
from moonleap.utils.case import upper0

from . import props
from .resources import ListView


@tags(["list-view"])
def create_list_view(term, block):
    name = kebab_to_camel(term.data)
    list_view = ListView(item_name=name, name=f"{upper0(name)}ListView")
    return list_view


@extend(ListView)
class ExtendListView:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
