import moonleap.resource.props as P
from moonleap import create_forward, extend, kebab_to_camel, kebab_to_snake, rule, tags
from moonleap.utils.case import snake_to_kebab
from moonleap.verbs import provides
from moonleap_django.module import Module

from .resources import ItemList


@tags(["item-list"])
def create_item_list(term, block):
    name_camel = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    item_list = ItemList(
        item_name_camel=name_camel,
        item_name_snake=name_snake,
    )
    return item_list


@rule("module", provides, "item-list")
def module_contains_item_list(module, item_list):
    kebab_name = snake_to_kebab(item_list.item_name_snake)
    return create_forward(module, provides, f"{kebab_name}:item-type")


@extend(Module)
class ExtendModule:
    item_lists_provided = P.children(provides, "item-list")
