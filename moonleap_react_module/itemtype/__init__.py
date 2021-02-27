import moonleap.resource.props as P
from moonleap import extend, tags
from moonleap.verbs import contains

from .resources import ItemType


@tags(["item-type"])
def create_item_type(term, block):
    item_type = ItemType(name=term.data)
    return item_type
