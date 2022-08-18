from moonleap import u0
from moonleap.typespec.form_type_spec_from_data_type_spec import (
    form_type_spec_from_data_type_spec,
)
from moonleap.typespec.type_spec_store import type_spec_store


def item_type_spec(item):
    return type_spec_store().get(item.type_name)


def item_type_name(item):
    return u0(item.item_name)


def item_form_type_spec(item):
    form_type_spec = type_spec_store().get(item.form_type_name)
    if form_type_spec:
        return form_type_spec

    form_type_spec = form_type_spec_from_data_type_spec(
        item.type_spec, item.form_type_name
    )
    type_spec_store().setdefault(item.form_type_name, form_type_spec)
    return form_type_spec


def item_form_type_name(item):
    return u0(item.item_name) + "Form"


def named_item_output_field_name(named_item):
    return named_item.name if named_item.name else named_item.typ.item_name
