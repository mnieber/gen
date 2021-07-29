import moonleap.resource.props as P
from moonleap import extend, kebab_to_camel, kebab_to_snake, tags
from moonleap.verbs import provides
from moonleap_django.module import Module

from .resources import ItemType


@tags(["item-type"])
def create_item_type(term, block):
    name_camel = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    item_type = ItemType(
        name_camel=name_camel,
        name_snake=name_snake,
    )
    return item_type


@extend(Module)
class ExtendModule:
    item_types = P.children(provides, "item-type")
