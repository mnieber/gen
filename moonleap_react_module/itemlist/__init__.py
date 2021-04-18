from moonleap import create_forward, kebab_to_camel, rule, tags
from moonleap.resource.rel import Forwards
from moonleap.verbs import contains, has

from .resources import ItemList


@tags(["item-list"])
def create_item_list(term, block):
    item_list = ItemList(item_name=kebab_to_camel(term.data))
    return item_list


@rule("store", contains, "item-list")
def store_contains_item_list(store, item_list):
    dataloader_term_str = f"{item_list.item_name}-list:dataloader"
    return Forwards(
        [
            create_forward(store, contains, f"{item_list.item_name}:item-type"),
            create_forward(store.module, has, dataloader_term_str),
        ]
    )
