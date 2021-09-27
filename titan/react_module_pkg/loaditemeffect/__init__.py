from pathlib import Path

from moonleap import MemFun, create, extend, rule
from moonleap.utils.case import kebab_to_camel
from moonleap.verbs import uses

from . import props
from .props import get_context
from .resources import LoadItemEffect


@create("load-item-effect", ["component"])
def create_load_item_effect(term, block):
    load_item_effect = LoadItemEffect(name=kebab_to_camel(term.data))
    load_item_effect.add_template_dir(Path(__file__).parent / "templates", get_context)
    return load_item_effect


@rule("item-view", uses, "load-item-effect")
def item_view_uses_load_item_effect(item_view, load_item_effect):
    load_item_effect.route_params = item_view._get_route_params()
    load_item_effect.item_name = item_view.item_name


@extend(LoadItemEffect)
class ExtendLoadItemEffect:
    create_router_configs = MemFun(props.create_router_configs)
