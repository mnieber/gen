from moonleap.typespec.type_spec_store import type_spec_store


def item_type_type_spec(item_type):
    return type_spec_store().get(item_type.name)
