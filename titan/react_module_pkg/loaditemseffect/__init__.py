from pathlib import Path

from moonleap import MemFun, create, extend, kebab_to_camel, rule
from moonleap.verbs import uses

from . import props
from .props import get_context
from .resources import LoadItemsEffect


@create("load-items-effect", ["component"])
def create_load_items_effect(term, block):
    load_items_effect = LoadItemsEffect(name=kebab_to_camel(term.data))
    load_items_effect.add_template_dir(Path(__file__).parent / "templates", get_context)
    return load_items_effect


@rule("list-view", uses, "load-items-effect")
def item_view_uses_load_items_effect(list_view, load_items_effect):
    load_items_effect.item_name = list_view.item_name


@extend(LoadItemsEffect)
class ExtendLoadItemsEffect:
    create_router_configs = MemFun(props.create_router_configs)
