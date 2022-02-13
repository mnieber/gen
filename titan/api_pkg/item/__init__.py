import moonleap.resource.props as P
from moonleap import (
    Prop,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    named,
    rule,
)
from moonleap.verbs import uses

from . import props
from .resources import Item

rules = [
    (("item", uses, "item~type"), empty_rule()),
    (("item", "hacks", "item"), empty_rule()),
    (("item", "hacks", "item~list"), empty_rule()),
]

base_tags = [
    ("item", ["pipeline-elm"]),
]


@create("item")
def create_item(term, block):
    name = kebab_to_camel(term.data)
    item = Item(item_name=name)
    return item


@create("x+item")
def create_named_item(term, block):
    return named(Item)()


@rule("item")
def item_created(item):
    return create_forward(item, uses, f"{item.item_name}:item~type")


@extend(Item)
class ExtendItem:
    item_type = P.child(uses, "item~type")
    type_spec = Prop(props.item_type_spec)


@extend(named(Item))
class ExtendNamedItem:
    output_field_name = Prop(props.named_item_output_field_name)
    type_spec = Prop(props.item_type_spec)
