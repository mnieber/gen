from moonleap.utils.inflect import plural


def return_value(state_provider, container, data, hint=None):
    if data in state_provider.named_items_provided:
        data_path = state_provider.get_data_path(data)
        maybe_expr = state_provider.maybe_expression(data)
        return f"maybe({maybe_expr})({data_path})" if maybe_expr else data_path

    if data in state_provider.named_item_lists_provided:
        data_path = state_provider.get_data_path(data)
        maybe_expr = state_provider.maybe_expression(data)
        return f"maybe({maybe_expr})({data_path}, [])" if maybe_expr else data_path

    if data in container and hint == "items":
        container = data
        named_item_list = data.named_item_list
        items_name = plural(container.item.item_name)
        assert named_item_list
        maybe_expr = state_provider.maybe_expression(named_item_list)
        data_path = f"state.{container.name}.data.{items_name}" + (
            "Display" if container.get_bvr("filtering") else ""
        )
        return f"maybe({maybe_expr}, [])({data_path})" if maybe_expr else data_path

    if data in container and hint == "highlighted_item":
        container = data
        named_item_list = data.named_item_list
        assert named_item_list
        maybe_expr = state_provider.maybe_expression(named_item_list)
        data_path = f"state.{container.name}.highlight.item"
        return f"maybe({maybe_expr})({data_path})" if maybe_expr else data_path
