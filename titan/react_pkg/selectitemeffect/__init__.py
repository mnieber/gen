
import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, empty_rule, extend, rule, u0
from moonleap.blocks.verbs import has
from moonleap.utils.case import kebab_to_camel

from .resources import SelectItemEffect

base_tags = {"select-item-effect": ["component"]}


@create("select-item-effect")
def create_select_item_effect(term):
    select_item_effect = SelectItemEffect(
        item_name=kebab_to_camel(term.data),
        name=kebab_to_camel(f"Select{u0(term.data)}Effect"),
    )
    return select_item_effect


@rule("select-item-effect")
def created_select_item_effect(select_item_effect):
    return create_forward(
        select_item_effect, has, f"{select_item_effect.item_name}:item~list"
    )


@extend(SelectItemEffect)
class ExtendSelectItemEffect:
    item_list = P.child(has, "item~list", required=True)


rules = {"select-item-effect": {(has, "item~list"): empty_rule()}}
