import moonleap.resource.props as P
from leapreact.component import Component
from leapreact.store import Store
from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import contains

from .resources import ItemList


@tags(["item-list"])
def create_item_list(term, block):
    item_list = ItemList(name=term.data)
    return item_list


@rule("store", contains, "item-list")
def service_has_router(app_module, router):
    pass


@extend(Store)
class ExtendStore:
    lists = P.children(contains, "item-list")
