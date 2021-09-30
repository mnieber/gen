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
from moonleap.verbs import provides, uses
from titan.api_pkg.itemlist.resources import ItemList

from .resources import Item


@create("item")
def create_item(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    item = Item(
        item_name=name,
        item_name_snake=name_snake,
    )
    return item


@rule("item")
def item_created(item):
    return create_forward(item, uses, f"{item.item_name}:item~type")


rules = [
    (("item", uses, "item~type"), empty_rule()),
    (("item", provides, "item"), empty_rule()),
    (("item", provides, "item~list"), empty_rule()),
]


@extend(Item)
class ExtendItem:
    item_type = P.child(uses, "item~type")
    items_provided = P.children(provides, "item")
    item_lists_provided = P.children(provides, "item~list")
    provider_items = P.parents("item", provides)


@extend(ItemList)
class ExtendItemList:
    provider_items = P.parents("item", provides)
