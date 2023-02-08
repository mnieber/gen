from moonleap import l0
from moonleap.utils.inflect import plural


def get_data_path(state_provider, data, state=None, hint=None):
    widget_spec = state_provider.widget_spec

    if data in state_provider.named_items_provided:
        named_item = data
        return widget_spec.get_data_path(named_item)

    if data in state_provider.named_item_lists_provided:
        named_item_list = data
        return widget_spec.get_data_path(named_item_list)

    if state:
        if data in state.containers and hint == "items":
            container = data
            items_name = plural(container.item.item_name)
            return f"{l0(state.name)}.{container.name}.data.{items_name}" + (
                "Display"
                if (container.get_bvr("filtering") or container.get_bvr("insertion"))
                else ""
            )

        if data in state.containers and hint == "highlighted_item":
            container = data
            return f"{l0(state.name)}.{container.name}.highlight.item"
