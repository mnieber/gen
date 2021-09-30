from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, create, empty_rule, extend, u0
from moonleap.utils.case import kebab_to_camel
from moonleap.verbs import uses
from titan.api_pkg.item.resources import Item

from . import props
from .resources import LoadItemEffect

base_tags = [
    ("load-item-effect", ["component", "api-effect"]),
]

rules = [(("item", uses, "load-item-effect"), empty_rule())]


@create("load-item-effect")
def create_load_item_effect(term, block):
    load_item_effect = LoadItemEffect(name=kebab_to_camel(u0(term.data)) + "Effect")
    load_item_effect.add_template_dir(
        Path(__file__).parent / "templates", props.get_context
    )
    return load_item_effect


@extend(LoadItemEffect)
class ExtendLoadItemEffect:
    create_router_configs = MemFun(props.create_router_configs)
    item = P.parent("item", uses, required=True)


@extend(Item)
class ExtendItem:
    react_load_effect = P.child(uses, "load-item-effect")
