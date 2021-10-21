import moonleap.resource.props as P
from moonleap import create, create_forward, empty_rule, extend, kebab_to_camel, rule
from moonleap.resource.named_class import named
from moonleap.verbs import uses
from titan.api_pkg.item.resources import Item

from .resources import ItemList


@create("item~list")
def create_item_list(term, block):
    name = kebab_to_camel(term.data)
    item_list = ItemList(item_name=name)
    return item_list


@create("x+item~list")
def create_named_item(term, block):
    return named(ItemList)(term, block)


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
