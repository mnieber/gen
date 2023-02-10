from moonleap import Prop, create, extend, kebab_to_camel, named
from titan.types_pkg.typeregistry.resources import Item

from . import props

base_tags = {
    "item": ["generic-item"],
}


@create("item")
def create_item(term):
    from titan.types_pkg.typeregistry import get_type_reg

    item_name = kebab_to_camel(term.data)
    return get_type_reg().get_item(item_name)


@extend(Item)
class ExtendItem:
    type_name = Prop(props.item_type_name)
