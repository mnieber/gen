from moonleap.typespec.type_spec_store import type_spec_store
from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList


def get_member_field_spec(parent_item, member_item):
    type_spec = type_spec_store().get(parent_item.item_type.name)
    for field_spec in type_spec.field_specs:
        if isinstance(member_item, Item):
            if field_spec.field_type == "fk":
                if field_spec.target_type_spec.type_name == member_item.item_type.name:
                    return field_spec
        if isinstance(member_item, ItemList):
            if field_spec.field_type == "relatedSet" and not field_spec.through:
                if field_spec.target_type_spec.type_name == member_item.item_type.name:
                    return field_spec
    raise Exception(f"get_member_field_spec: Not found {parent_item} {member_item}")
