from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, create, empty_rule, extend, kebab_to_camel, rule, u0
from moonleap.verbs import uses
from titan.api_pkg.itemlist.resources import ItemList

from . import props
from .props import get_context
from .resources import LoadItemsEffect

base_tags = [("load-items-effect", ["component", "api-effect"])]

rules = [(("item~list", uses, "load-items-effect"), empty_rule())]


@create("load-items-effect")
def create_load_items_effect(term, block):
    load_items_effect = LoadItemsEffect(name=kebab_to_camel(u0(term.data)) + "Effect")
    load_items_effect.add_template_dir(Path(__file__).parent / "templates", get_context)
    return load_items_effect


@extend(LoadItemsEffect)
class ExtendLoadItemsEffect:
    create_router_configs = MemFun(props.create_router_configs)
    item_list = P.parent("item~list", uses, required=True)


@extend(ItemList)
class ExtendItemList:
    react_load_effect = P.child(uses, "load-items-effect")
