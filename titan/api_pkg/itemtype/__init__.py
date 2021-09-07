from moonleap import create, kebab_to_camel, kebab_to_snake

from .resources import ItemType


@create("item-type", [])
def create_item_type(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    item_type = ItemType(
        name=name,
        name_snake=name_snake,
    )
    return item_type
