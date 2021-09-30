import moonleap.resource.props as P
from moonleap import (
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    kebab_to_snake,
    rule,
)
from moonleap.verbs import uses
from titan.api_pkg.item.resources import Item

from .resources import ItemList


@create("item~list")
def create_item_list(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    item_list = ItemList(
        item_name=name,
        item_name_snake=name_snake,
    )
    return item_list


@rule("item~list")
def item_list_created(item_list):
    return create_forward(item_list, uses, f"{item_list.item_name}:item")


rules = [(("item~list", uses, "item"), empty_rule())]


@extend(ItemList)
class ExtendItemList:
    item = P.child(uses, "item", required=True)


@extend(Item)
class ExtendItem:
    item_list = P.parent("item~list", uses, required=True)
