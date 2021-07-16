from dataclasses import dataclass

from moonleap.utils.case import upper0
from moonleap_react.component import Component
from moonleap_react_module.loaditemseffect import LoadItemsEffect


@dataclass
class ListView(Component):
    item_name: str
    items_name: str


def create_load_items_effect(list_view):
    name = f"Load{upper0(list_view.items_name)}Effect"
    load_items_effect = LoadItemsEffect(item_name=list_view.item_name, name=name)
    return load_items_effect
