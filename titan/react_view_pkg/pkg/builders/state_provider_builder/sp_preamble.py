from moonleap.utils import chop0
from moonleap.utils.inflect import plural

sp_preamble_tpl = chop0(
    """
{% magic_with state.name as MyState %}
{% magic_with container.item.item_name as containerItem %}
{% magic_with named_item_list.typ.item_name as myNamedListItem %}
{% magic_with container.name as myContainer %}
    const getDefaultPropsContext = () => {
      const result = { defaultProps: {} };

      result.defaultProps = {
        ...result.defaultProps,
        myNamedItem: () => {{ __.return_value(named_item) }},                                                      {% !! named_item in state_provider.named_items_provided %}
        myNamedListItems: () => {{ __.return_value(named_item_list) }},                                            {% !! named_item_list in state_provider.named_item_lists_provided %}
        myState: () => state,                                                                                   {% if state %}
        containerItems: () => {{ __.return_value(container, "items") }},                                           {% for container in state.containers %}{% ?? container.named_item_list %}
        containerItem: () => {{ __.return_value(container, "highlighted_item") }},                                 {% ?? container.get_bvr("highlight") %}
        containerItemsDeletion: () => state.myContainer.deletion,                                               {% ?? container.get_bvr("deletion") %}
        containerItemsDragAndDrop: () => state.myContainer.dragAndDrop,                                         {% ?? container.get_bvr("dragAndDrop") %}
        containerItemsFiltering: () => state.myContainer.filtering,                                             {% ?? container.get_bvr("filtering") %}
        containerItemsHighlight: () => state.myContainer.highlight,                                             {% ?? container.get_bvr("highlight") %}
        containerItemsSelection: () => state.myContainer.selection,                                             {% ?? container.get_bvr("selection") %}{% endfor %}{% endif %}
      };

      return result;
    };
    {{ "" }}
{% end_magic_with %}
{% end_magic_with %}
{% end_magic_with %}
{% end_magic_with %}
    """
)


def return_value(state_provider, containers, data, hint=None):
    if data in state_provider.named_items_provided:
        data_path = state_provider.get_data_path(data)
        maybe_expr = state_provider.maybe_expression(data)
        return f"maybe({maybe_expr})({data_path})" if maybe_expr else data_path

    if data in state_provider.named_item_lists_provided:
        data_path = state_provider.get_data_path(data)
        maybe_expr = state_provider.maybe_expression(data)
        return f"maybe({maybe_expr})({data_path}, [])" if maybe_expr else data_path

    if data in containers and hint == "items":
        container = data
        named_item_list = data.named_item_list
        items_name = plural(container.item.item_name)
        assert named_item_list
        maybe_expr = state_provider.maybe_expression(named_item_list)
        data_path = f"state.{container.name}.data.{items_name}Display"
        return f"maybe({maybe_expr}, [])({data_path})" if maybe_expr else data_path

    if data in containers and hint == "highlighted_item":
        container = data
        named_item_list = data.named_item_list
        assert named_item_list
        maybe_expr = state_provider.maybe_expression(named_item_list)
        data_path = f"state.{container.name}.highlight.item"
        return f"maybe({maybe_expr})({data_path})" if maybe_expr else data_path
