from moonleap import create_forward, kebab_to_camel, rule, tags
from moonleap.verbs import contains

from .resources import Item


@tags(["item"])
def create_item(term, block):
    item = Item(item_name=kebab_to_camel(term.data))
    return item


@rule("store", contains, "item")
def store_contains_item_list(store, item_list):
    return create_forward(store, contains, f"{item_list.item_name}:item-type")
