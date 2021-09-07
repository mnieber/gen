from pathlib import Path

from moonleap import MemFun, extend, upper0
from moonleap.parser.term import Term
from moonleap.resource import ResourceMetaData

from . import props
from .props import get_context
from .resources import LoadItemsEffect


def create_load_items_effect(list_view):
    # TODO can we use _create_resource for this?
    name = f"Load{upper0(list_view.items_name)}Effect"
    term = Term(list_view.item_name, "load-items-effect")
    load_items_effect = LoadItemsEffect(item_name=list_view.item_name, name=name)
    load_items_effect._meta = ResourceMetaData(
        term, list_view._meta.block, ["component"]
    )
    load_items_effect.add_template_dir(Path(__file__).parent / "templates", get_context)
    return load_items_effect


@extend(LoadItemsEffect)
class ExtendLoadItemsEffect:
    create_router_configs = MemFun(props.create_router_configs)
