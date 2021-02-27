import moonleap.resource.props as P
from moonleap import extend, tags
from moonleap.verbs import contains
from moonleap_react_module.store import Store

from .resources import Item


@tags(["item"])
def create_item(term, block):
    item = Item(name=term.data)
    return item


@extend(Store)
class ExtendStore:
    items = P.children(contains, "item")
