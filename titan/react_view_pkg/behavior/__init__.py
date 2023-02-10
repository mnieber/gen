import moonleap.packages.extensions.props as P
from moonleap import (
    create,
    create_forward,
    empty_rule,
    extend,
    get_root_resource,
    kebab_to_camel,
    named,
    rule,
)
from moonleap.blocks.verbs import has
from titan.types_pkg.item import Item

from .resources import Behavior, DeletionBehavior, EditingBehavior, InsertionBehavior

base_tags = {
    "addition": ["behavior"],
    "deletion": ["behavior"],
    "drag-and-drop": ["behavior"],
    "editing": ["behavior"],
    "filtering": ["behavior"],
    "highlight": ["behavior"],
    "insertion": ["behavior"],
    "selection": ["behavior"],
}

rules = {
    ("x+item~list", has, "behavior"): empty_rule(),
    ("item", has, "addition"): empty_rule(),
}


@create("behavior")
def create_behavior(term):
    has_param = term.tag in ("selection", "filtering", "highlight", "insertion")
    return Behavior(
        item_name=kebab_to_camel(term.data),
        name=kebab_to_camel(term.tag),
        has_param=has_param,
    )


@create("addition")
def create_addition_behavior(term):
    item_name = kebab_to_camel(term.data)
    return Behavior(
        item_name=item_name,
        name=kebab_to_camel(term.tag),
        has_param=True,
    )


@create("editing")
def create_editing_behavior(term):
    return EditingBehavior(
        item_name=kebab_to_camel(term.data),
        name=kebab_to_camel(term.tag),
        has_param=False,
    )


@create("deletion")
def create_deletion_behavior(term):
    return DeletionBehavior(
        item_name=kebab_to_camel(term.data),
        name=kebab_to_camel(term.tag),
        has_param=False,
    )


@create("insertion")
def create_insertion_behavior(term):
    return InsertionBehavior(
        item_name=kebab_to_camel(term.data),
        name=kebab_to_camel(term.tag),
        has_param=True,
    )


@rule("addition")
def created_addition(addition):
    item_term_str = f"{addition.item_name}:item"
    return create_forward(item_term_str, has, addition)


@rule("selection")
def created_selection(selection):
    get_root_resource().set_flags(["utils/mergeClickHandlers"])


@extend(Item)
class ExtendItem:
    addition = P.child(has, "addition")
