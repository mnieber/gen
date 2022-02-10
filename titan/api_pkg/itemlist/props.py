from moonleap.typespec.type_spec_store import type_spec_store


def item_list_type_spec(item_list):
    return type_spec_store().get(item_list.item_type.name)


def item_list_item_type(item_list):
    return item_list.item.item_type


def named_item_list_output_field_name(named_item_list):
    return (
        named_item_list.name if named_item_list.name else named_item_list.typ.item_name
    )
