from moonleap import Rel, rule, tags, word_to_term
from moonleap.verbs import contains

from .resources import ItemList


@tags(["item-list"])
def create_item_list(term, block):
    item_list = ItemList(item_name=term.data)
    return item_list


@rule("store", contains, "item-list")
def store_contains_item_list(store, item_list):
    item_type_term = word_to_term(f"{item_list.item_name}:item-type")
    return Rel(store.term, contains, item_type_term)
