from moonleap import l0
from moonleap.utils.inflect import plural


def get_return_value(state_provider, state, data, hint=None):
    widget_spec = state_provider.widget_spec

    if data in state_provider.named_items_provided:
        data_path = widget_spec.get_data_path(data)
        maybe_expr = widget_spec.maybe_expression(data)
        item_name = data.typ.item_name
        return f"cache.{item_name})" if maybe_expr else data_path

    if data in state_provider.named_item_lists_provided:
        data_path = widget_spec.get_data_path(data)
        maybe_expr = widget_spec.maybe_expression(data)
        items_name = plural(data.typ.item_name)
        return f"cache.{items_name}" if maybe_expr else data_path

    if data in state.containers and hint == "items":
        container = data
        named_item_list = data.named_item_list
        items_name = plural(container.item.item_name)
        assert named_item_list
        maybe_expr = widget_spec.maybe_expression(named_item_list)
        data_path = f"{l0(state.name)}.{container.name}.data.{items_name}" + (
            "Display"
            if (container.get_bvr("filtering") or container.get_bvr("insertion"))
            else ""
        )
        return f"cache.{items_name}" if maybe_expr else data_path

    if data in state.containers and hint == "highlighted_item":
        container = data
        named_item_list = data.named_item_list
        assert named_item_list
        maybe_expr = widget_spec.maybe_expression(named_item_list)
        data_path = f"{l0(state.name)}.{container.name}.highlight.item"
        item_name = container.item.item_name
        return f"cache.{item_name}" if maybe_expr else data_path
