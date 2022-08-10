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
from titan.api_pkg.itemtype.resources import ItemType

from . import props
from .resources import Item

rules = [(("item", uses, "item~type"), empty_rule())]

base_tags = [
    ("item", ["pipeline-elm"]),
]


@create("item")
def create_item(term):
    name = kebab_to_camel(term.data)
    item = Item(item_name=name)
    return item


@create("x+item")
def create_named_item(term):
    return named(Item)()


@rule("item")
def item_created(item):
    return create_forward(item, uses, f"{item.meta.term.data}:item~type")


@extend(Item)
class ExtendItem:
    item_type = P.child(uses, "item~type")
    type_spec = Prop(props.item_type_spec)


@extend(ItemType)
class ExtendItemType:
    item = P.parent("item~type", uses)


@extend(named(Item))
class ExtendNamedItem:
    output_field_name = Prop(props.named_item_output_field_name)
    type_spec = Prop(props.item_type_spec)
