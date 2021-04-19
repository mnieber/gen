from moonleap import create_forward, kebab_to_camel, rule, tags
from moonleap.verbs import contains, has

from .resources import Item


@tags(["item"])
def create_item(term, block):
    item = Item(name=kebab_to_camel(term.data))
    return item


@rule("store", contains, "item")
def store_contains_item(store, item):
    dataloader_term_str = f"{item.name}:dataloader"
    return [
        create_forward(store, contains, f"{item.name}:item-type"),
        create_forward(store.module, has, dataloader_term_str),
    ]
