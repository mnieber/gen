import moonleap.resource.props as P
from moonleap import create_forward, extend, kebab_to_camel, kebab_to_snake, rule, tags
from moonleap.utils.case import snake_to_kebab
from moonleap.verbs import provides, receives
from moonleap_django.module import Module

from .resources import Item


@tags(["item"])
def create_item(term, block):
    name_camel = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    item = Item(
        item_name_camel=name_camel,
        item_name_snake=name_snake,
    )
    return item


@rule("module", receives, "item")
def module_receives_item(module, item):
    kebab_name = snake_to_kebab(item.item_name_snake)
    return create_forward(module, provides, f"{kebab_name}:item-type")


@extend(Module)
class ExtendModule:
    items_received = P.children(receives, "item")
