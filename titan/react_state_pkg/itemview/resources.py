from dataclasses import dataclass

from moonleap import upper0
from titan.react_module_pkg.loaditemeffect.resources import (
    LoadItemEffect,
    create_name_postfix,
)
from titan.react_pkg.component import Component
from titan.react_state_pkg.selectitemeffect.resources import SelectItemEffect


@dataclass
class ItemView(Component):
    item_name: str


def create_load_item_effect(item_view, route_params):
    by = create_name_postfix(item_view.item_name, route_params)
    name = f"Load{upper0(item_view.item_name)}{by}Effect"
    loadItemEffect = LoadItemEffect(
        item_name=item_view.item_name, route_params=route_params, name=name
    )
    return loadItemEffect


def create_select_item_effect(item_view, route_params):
    name = f"Select{upper0(item_view.item_name)}Effect"
    select_item_effect = SelectItemEffect(item_name=item_view.item_name, name=name)
    return select_item_effect
