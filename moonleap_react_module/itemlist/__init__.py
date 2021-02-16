import moonleap.resource.props as P
from moonleap import extend, rule, tags
from moonleap.verbs import contains
from moonleap_react_module.store import Store

from .resources import ItemList


@tags(["item-list"])
def create_item_list(term, block):
    item_list = ItemList(item_name=term.data)
    return item_list


@rule("store", contains, "item-list")
def store_contains_item_list(store, item_list):
    pass


@extend(Store)
class ExtendStore:
    lists = P.children(contains, "item-list")
