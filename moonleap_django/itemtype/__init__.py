import moonleap.resource.props as P
from moonleap import extend, kebab_to_camel, rule, tags
from moonleap.verbs import provides
from moonleap_django.module import Module

from .resources import ItemType


@tags(["item-type"])
def create_item_type(term, block):
    item_type = ItemType(name=kebab_to_camel(term.data))
    return item_type


@rule("module", provides, "item-type")
def module_provides_item_type(module, item_type):
    pass


@extend(ItemType)
class ExtendItemType:
    pass


@extend(Module)
class ExtendModule:
    item_types = P.children(provides, "item-type")
