from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, create, create_forward, extend, kebab_to_camel, rule
from moonleap.utils.case import upper0
from moonleap.verbs import has, uses
from titan.react_module_pkg.loaditemeffect import create_load_item_effect

from . import props
from .resources import ItemView, create_select_item_effect


@create("item-view", ["component"])
def create_item_view(term, block):
    name = kebab_to_camel(term.data)
    item_view = ItemView(item_name=name, name=f"{upper0(name)}View")
    item_view.add_template_dir(Path(__file__).parent / "templates")
    return item_view


@extend(ItemView)
class ExtendItemView:
    _get_route_params = MemFun(props._get_route_params)
    create_router_configs = MemFun(props.create_router_configs)
    load_item_effect = P.child(uses, "load-item-effect")
    select_item_effect = P.child(uses, "select-item-effect")
