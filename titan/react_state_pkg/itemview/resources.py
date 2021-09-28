from dataclasses import dataclass

from moonleap import u0
from titan.react_pkg.component import Component
from titan.react_state_pkg.selectitemeffect.resources import SelectItemEffect


@dataclass
class ItemView(Component):
    item_name: str


def create_select_item_effect(item_view, route_params):
    name = f"Select{u0(item_view.item_name)}Effect"
    select_item_effect = SelectItemEffect(item_name=item_view.item_name, name=name)
    return select_item_effect
