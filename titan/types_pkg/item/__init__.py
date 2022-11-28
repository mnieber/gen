from moonleap import Prop, create, extend, kebab_to_camel, named

from . import props
from .resources import Item

base_tags = {
    "item": ["pipeline-elm", "generic-item"],
}


@create("item")
def create_item(term):
    item_name = kebab_to_camel(term.data)
    item = Item(item_name=item_name)
    return item


@create("x+item")
def create_named_item(term):
    return named(Item)()


@extend(Item)
class ExtendItem:
    type_name = Prop(props.item_type_name)
    type_spec = Prop(props.item_type_spec)


@extend(named(Item))
class ExtendNamedItem:
    output_field_name = Prop(props.named_item_output_field_name)
    type_spec = Prop(props.item_type_spec)
