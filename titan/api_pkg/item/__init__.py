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
    u0,
)
from moonleap.typespec.default_field_specs_store import create_fk_field_spec
from moonleap.verbs import provides, uses
from titan.api_pkg.itemlist.resources import ItemList

from . import props
from .resources import Item

rules = [(("item", uses, "item~type"), empty_rule())]


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


@rule("item", provides, "item")
def item_provides_item(provider_item, item):
    from moonleap.typespec.type_spec_store import type_spec_store

    type_spec_store().register_default_field_spec(
        # Note: we cannot use provider_item.item_type due to a race condition
        type_name=u0(provider_item.item_name),
        field_spec=create_fk_field_spec(item.item_name),
    )


@rule("item", provides, "item~list")
def item_provides_item_list(provider_item, item_list):
    from moonleap.typespec.type_spec_store import type_spec_store

    type_spec_store().register_default_field_spec(
        # Note: we cannot use provider_item.item_type due to a race condition
        type_name=u0(item_list.item_name),
        field_spec=create_fk_field_spec(provider_item.item_name),
    )


@extend(Item)
class ExtendItem:
    item_type = P.child(uses, "item~type")
    items_provided = P.children(provides, "item")
    item_lists_provided = P.children(provides, "item~list")
    provider_items = P.parents("item", provides)
    type_spec = Prop(props.item_type_spec)


@extend(ItemList)
class ExtendItemList:
    provider_items = P.parents("item", provides)


@extend(named(Item))
class ExtendNamedItem:
    output_field_name = Prop(props.named_item_output_field_name)
    type_spec = Prop(props.item_type_spec)
