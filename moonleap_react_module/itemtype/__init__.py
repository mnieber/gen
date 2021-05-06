import moonleap.resource.props as P
from moonleap import Prop, StoreOutputPaths, extend, kebab_to_camel, tags
from moonleap.verbs import contains
from moonleap_react_module.store import Store

from . import props
from .resources import ItemType


@tags(["item-type"])
def create_item_type(term, block):
    item_type = ItemType(name=kebab_to_camel(term.data))
    return item_type


@extend(ItemType)
class ExtendItemType(StoreOutputPaths):
    store = P.parent(Store, contains, "item-type")
    module_path = Prop(props.module_path)
