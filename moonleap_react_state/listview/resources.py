from dataclasses import dataclass

from moonleap.utils.case import upper0
from moonleap.utils.inflect import plural
from moonleap_react.component import Component
from moonleap_react_module.loaditemseffect import LoadItemsEffect


@dataclass
class ListView(Component):
    item_name: str


def create_load_items_effect(list_view):
    name = f"Load{upper0(plural(list_view.item_name))}Effect"
    load_items_effect = LoadItemsEffect(item_name=list_view.item_name, name=name)
    return load_items_effect
