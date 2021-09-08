import moonleap.resource.props as P
from moonleap import kebab_to_camel, kebab_to_snake, tags

from .resources import ItemList


@tags(["item-list"])
def create_item_list(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    item_list = ItemList(
        item_name=name,
        item_name_snake=name_snake,
    )
    return item_list
