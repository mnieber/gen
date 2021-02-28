import moonleap.resource.props as P
from moonleap import MemFun, StoreOutputPaths, extend, render_templates, rule, tags
from moonleap.verbs import contains
from moonleap_react_module.store import Store

from .resources import ItemType


@tags(["item-type"])
def create_item_type(term, block):
    item_type = ItemType(name=term.data)
    return item_type


@rule("store", contains, "item-type")
def store_contains_item_type(store, item_type):
    if not item_type.output_path:
        item_type.output_paths.add_source(store.module)


@extend(ItemType)
class ExtendItemType(StoreOutputPaths):
    render = MemFun(render_templates(__file__))
    store = P.parent(Store, contains, "item-type")
