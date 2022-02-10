from moonleap.typespec.type_spec_store import type_spec_store


def item_type_spec(item):
    return type_spec_store().get(item.item_type.name)


def named_item_output_field_name(named_item):
    return named_item.name if named_item.name else named_item.typ.item_name
