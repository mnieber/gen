from moonleap import Rel, kebab_to_camel, rule, tags, word_to_term
from moonleap.verbs import contains

from .resources import Item


@tags(["item"])
def create_item(term, block):
    item = Item(name=kebab_to_camel(term.data))
    return item


@rule("store", contains, "item")
def store_contains_item(store, item):
    item_type_term = word_to_term(f"{item.name}:item-type")
    return Rel(store.term, contains, item_type_term)
