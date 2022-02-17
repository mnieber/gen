from moonleap import Prop, create, extend, kebab_to_camel, u0

from . import props
from .resources import ItemType


@create("item~type")
def create_item_type(term):
    name = kebab_to_camel(term.data)
    item_type = ItemType(name=u0(name))
    return item_type


@extend(ItemType)
class ExtendItemType:
    type_spec = Prop(props.item_type_type_spec)
