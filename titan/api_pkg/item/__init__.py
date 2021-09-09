from moonleap import kebab_to_camel, kebab_to_snake, tags

from .resources import Item


@tags(["item"])
def create_item(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    item = Item(
        item_name=name,
        item_name_snake=name_snake,
    )
    return item
