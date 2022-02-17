import moonleap.resource.props as P
from moonleap import (
    Prop,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    named,
    rule,
)
from moonleap.verbs import uses
from titan.api_pkg.item.resources import Item

from . import props
from .resources import ItemList

base_tags = [
    ("item~list", ["pipeline-elm"]),
]

rules = [(("item~list", uses, "item"), empty_rule())]


@create("item~list")
def create_item_list(term):
    name = kebab_to_camel(term.data)
    item_list = ItemList(item_name=name)
    return item_list


@create("x+item~list")
def create_named_item(term):
    return named(ItemList)()


@rule("item~list")
def item_list_created(item_list):
    return create_forward(item_list, uses, f"{item_list.item_name}:item")


@extend(ItemList)
class ExtendItemList:
    item = P.child(uses, "item", required=True)
    item_type = Prop(props.item_list_item_type)
    type_spec = Prop(props.item_list_type_spec)


@extend(Item)
class ExtendItem:
    item_list = P.parent("item~list", uses)


@extend(named(ItemList))
class ExtendNamedItemList:
    output_field_name = Prop(props.named_item_list_output_field_name)
