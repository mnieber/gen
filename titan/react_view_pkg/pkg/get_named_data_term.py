from moonleap import kebab_to_camel, named
from moonleap.parser.utils.get_meta import get_meta
from titan.types_pkg.item import Item
from titan.types_pkg.itemlist import ItemList
from titan.types_pkg.typeregistry import get_type_reg


def _get_named_data_term(widget_spec, name):
    value = widget_spec.get_value_by_name(name)
    if value and "+" not in value:
        raise Exception(f"Expected + in value: {value}")
    return value if value else None


def get_named_item_list(widget_spec):
    term_str = _get_named_data_term(widget_spec, "items")
    if not term_str:
        return None

    named_item_list = named(ItemList)()
    named_item_list.meta = get_meta(term_str)
    term = named_item_list.meta.term
    item_name = kebab_to_camel(term.data)
    named_item_list.typ = get_type_reg().get_item_list(item_name)
    named_item_list.name = term.name

    return named_item_list


def get_named_item(widget_spec):
    term_str = _get_named_data_term(widget_spec, "item")
    if not term_str:
        return None

    named_item = named(Item)()
    named_item.meta = get_meta(term_str)
    term = named_item.meta.term
    item_name = kebab_to_camel(term.data)
    named_item.typ = get_type_reg().get_item(item_name)
    named_item.name = term.name

    return named_item
