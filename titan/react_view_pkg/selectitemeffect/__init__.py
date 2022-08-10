from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, empty_rule, extend, u0
from moonleap.utils.case import kebab_to_camel
from moonleap.verbs import uses
from titan.api_pkg.itemlist.resources import ItemList

from .resources import SelectItemEffect

base_tags = [("select-item-effect", ["component", "api-effect"])]


rules = [(("item~list", uses, "select-item-effect"), empty_rule())]


@create("select-item-effect")
def create_select_item_effect(term):
    select_item_effect = SelectItemEffect(
        name=kebab_to_camel(u0(term.data)) + "Effect",
    )
    select_item_effect.template_dir = Path(__file__).parent / "templates"
    return select_item_effect


@extend(SelectItemEffect)
class ExtendSelectItemEffect:
    item_list = P.parent("item~list", uses, required=True)


@extend(ItemList)
class ExtendItemList:
    react_select_effect = P.child(uses, "select-item-effect")
