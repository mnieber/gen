import moonleap.resource.props as P
from moonleap import extend, tags
from moonleap.verbs import contains
from moonleap_react_module.store import Store

from .resources import ItemType


@tags(["item-type"])
def create_item_type(term, block):
    item_type = ItemType(name=term.data)
    return item_type


@extend(ItemType)
class ExtendItemType:
    store = P.parent(Store, contains, "item-type")
