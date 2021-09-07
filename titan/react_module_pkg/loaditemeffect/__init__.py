from pathlib import Path

from moonleap import MemFun, extend, upper0
from moonleap.parser.term import Term
from moonleap.resource import ResourceMetaData

from . import props
from .props import get_context
from .resources import LoadItemEffect, create_name_postfix


def create_load_item_effect(item_view, route_params):
    # TODO can we use _create_resource for this?
    by = create_name_postfix(item_view.item_name, route_params)
    name = f"Load{upper0(item_view.item_name)}{by}Effect"
    term = Term(item_view.item_name, "load-item-effect")
    load_item_effect = LoadItemEffect(
        item_name=item_view.item_name, route_params=route_params, name=name
    )
    load_item_effect._meta = ResourceMetaData(
        term, item_view._meta.block, ["component"]
    )
    load_item_effect.add_template_dir(Path(__file__).parent / "templates", get_context)
    return load_item_effect


@extend(LoadItemEffect)
class ExtendLoadItemEffect:
    create_router_configs = MemFun(props.create_router_configs)
