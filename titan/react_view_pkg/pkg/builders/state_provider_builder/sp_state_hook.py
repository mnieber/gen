from moonleap import u0
from moonleap.utils import chop0
from moonleap.utils.inflect import plural
from titan.types_pkg.typeregistry import get_type_reg

sp_state_hook_tpl = chop0(
    """
{% magic_with state.name as MyState %}
{% magic_with container.item.item_name as containerItem %}
    const [state] = React.useState(() => new MyState({                                                          {% if state %}
      deleteContainerItems: (ids: string[]) => {                                                                {% for container in containers %}{% with d = __.delete_items_data(container) %}{% if d.deletes_items %}
        R.map(setToUpdating, lookUp(ids, state.containerItems.data.containerItemById));
        return {{ d.deleteMyItems }}.mutateAsync({ {{ d.myItemIds }}: ids });                                   {% if d.get('deleteMyItems') %}
        return Promise.all(R.map(                                                                               {% else %}
          (x: string) => {{ d.deleteMyItem }}.mutateAsync({ {{ d.myItemId }}: x }),
          ids));                                                                                                {% endif %}
      },                                                                                                        {% endif %}{% endwith %}
      saveContainerItemOrdering: (containerItems: ContainerItemT[]) => {                                        {% with d = __.order_items_data(container) %}{% if d.orders_items %}
        return {{ d.orderMyItems }}.mutateAsync({
          // {{ otherKey }}: Moonleap Todo,                                                                     {% !! otherKey in d.otherKeys %}
          {{ d.myItemIds }}: getIds({{ d.myItems }}),
        });
      },                                                                                                        {% endif %}{% endwith %}{% endfor %}
    }));                                                                                                        {% endif %}
{% end_magic_with %}
{% end_magic_with %}
    """
)


def delete_items_data(container):
    deletes_items = container.get_bvr("deletion")
    data = dict(deletes_items=deletes_items)

    if deletes_items:
        if container.delete_items_mutation:
            data["deleteMyItems"] = container.delete_items_mutation.name
            data["myItemIds"] = _get_field_name(
                container.delete_items_mutation, ["uuid[]"]
            )
        elif container.delete_item_mutation:
            data["deleteMyItem"] = container.delete_item_mutation.name
            data["myItemId"] = _get_field_name(
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
                data["orderMyItems"] = mutation.name
                data["myItems"] = plural(container.item.item_name)
                data["myItemIds"] = ids_field_name
    return data


def _get_field_name(mutation, field_types):
    for field_type in field_types:
        for field in mutation.api_spec.get_inputs([field_type]):
            return field.name
    raise Exception("Unknown field name")
