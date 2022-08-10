from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList


def get_member_field_spec(parent_item, member_item):
    for field_spec in parent_item.item_type.type_spec.field_specs:
        if isinstance(member_item, Item):
            if field_spec.field_type == "fk":
                if field_spec.target_type_spec.type_name == member_item.item_type.name:
                    return field_spec
        if isinstance(member_item, ItemList):
            if field_spec.field_type == "relatedSet":
                if field_spec.target_type_spec.type_name == member_item.item_type.name:
                    return field_spec
    raise Exception(f"get_member_field_spec: Not found {parent_item} {member_item}")
