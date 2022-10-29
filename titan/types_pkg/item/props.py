from moonleap import u0
from titan.types_pkg.typeregistry import get_type_reg


def item_type_spec(item):
    return get_type_reg().get(item.type_name)


def item_type_name(item):
    return u0(item.item_name)


def item_form_type_spec(item):
    return get_type_reg().get(item.form_type_name)


def item_form_type_name(item):
    return u0(item.item_name) + "Form"


def named_item_output_field_name(named_item):
    return named_item.name if named_item.name else named_item.typ.item_name
