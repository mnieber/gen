from moonleap import u0
from moonleap.utils.inflect import plural
from titan.types_pkg.typeregistry import get_type_reg


def delete_items_data(container):
    deletes_items = container.get_bvr("deletion")
    data = dict(deletes_items=deletes_items)

    if deletes_items:
        if container.delete_items_mutation:
            data["deleteMyCtrItems"] = container.delete_items_mutation.name
            data["myCtrItemIds"] = _get_field_name(
                container.delete_items_mutation, ["uuid[]"]
            )
        elif container.delete_item_mutation:
            data["deleteMyCtrItem"] = container.delete_item_mutation.name
            data["myCtrItemId"] = _get_field_name(
                container.delete_item_mutation, ["uuid", "string"]
            )
    return data


def order_items_data(container):
    mutation = container.order_items_mutation
    orders_items = container.get_bvr("dragAndDrop") and mutation
    data = dict(orders_items=orders_items)
    if orders_items:
        for (
            parent_type_name,
            parent_key,
        ) in mutation.api_spec.orders:
            field_spec = (
                get_type_reg()
                .get(u0(parent_type_name))
                .get_field_spec_by_key(parent_key)
            )

            if field_spec.target == container.item.type_spec.type_name:
                ids_field_name = _get_field_name(mutation, ["uuid[]"])
                data["otherKeys"] = [
                    x.key
                    for x in mutation.api_spec.get_inputs()
                    if x.key != ids_field_name
                ]
                data["orderMyCtrItems"] = mutation.name
                data["myCtrItems"] = plural(container.item.item_name)
                data["myCtrItemIds"] = ids_field_name
    return data


def save_item_data(container):
    mutation = container.save_item_mutation
    saves_item = container.get_bvr("editing") and mutation
    data = dict(saves_item=saves_item)
    data["saveMyCtrItem"] = mutation.name
    return data


def _get_field_name(mutation, field_types):
    for field_type in field_types:
        for field in mutation.api_spec.get_inputs([field_type]):
            return field.name
    raise Exception("Unknown field name")
