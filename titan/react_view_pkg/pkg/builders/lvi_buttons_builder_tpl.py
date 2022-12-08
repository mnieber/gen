from moonleap.utils import chop0

lvi_buttons_tpl = chop0(
    """
        <div                                                                            {% if bvrs_has_deletion %}
          className={cn(
            'TodoListViewItem__Buttons',
            'flex flex-row justify-end items-center'
          )}
        >
          <button
            className={smallButton}
            onClick={() => {
              props.onDelete();
            }}
          >
            Delete
          </button>
        </div>                                                                          {% endif %}
    """
)

lvi_buttons_props_tpl = chop0(
    """
onDelete: Function;                                                                     {% ?? bvrs_has_deletion %}
  """
)

lvi_buttons_add_props_tpl = chop0(
    """
& ClickHandlersT                                                                        {% ?? bvrs_has_selection %}
& DragHandlersT                                                                         {% ?? bvrs_has_drag_and_drop %}
  """
)

lvi_buttons_preamble_tpl = chop0(
    """
{% magic_with item_name as myItemName %}
if (isUpdating(props.myItemName)) {
  return UIkit && <div data-uk-spinner className=""></div>;                             {% ?? uikit %}
  return null;                                                                          {% ?? not uikit %}
}
{{ "" }}
{% end_magic_with %}
  """
)

lvi_buttons_imports_tpl = chop0(
    """
import { smallButton } from 'src/frames/components';
  """
)
