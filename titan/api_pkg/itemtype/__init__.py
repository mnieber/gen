from moonleap import create, kebab_to_camel

from .resources import ItemType


@create("item~type")
def create_item_type(term, block):
    name = kebab_to_camel(term.data)
    item_type = ItemType(name=name)
    return item_type
