from moonleap.utils import chop0

lvi_fields_tpl = chop0(
    """
{% magic_with _.component.item_name as myItemName %}
{% magic_with field_spec.name as fieldSpecName %}
        <div>                                                                           {% for field_spec in fields %}{% if field_spec.display %}
          {props.myItemName.fieldSpecName}                                              {% ?? field_spec.field_type not in ("boolean",) %}
          fieldSpecName: {props.myItemName.fieldSpecName ? 'Yes' : 'No'}                {% ?? field_spec.field_type in ("boolean",) %}
        </div>                                                                          {% endif %}{% endfor %}
{% end_magic_with %}
{% end_magic_with %}
"""
)

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

lvi_buttons_imports_tpl = chop0(
    """
import { smallButton } from 'src/frames/components';
  """
)

lvi_body_imports_tpl = chop0(
    """
import { dragHandlers, type DragHandlersT } from 'skandha-facets/DragAndDrop';                      {% ?? bvrs_has_drag_and_drop %}
import { clickHandlers, ClickHandlersT } from 'skandha-facets/handlers/ClickToSelectItems';         {% ?? bvrs_has_selection %}
  """
)

lvi_buttons_props_tpl = chop0(
    """
onDelete: Function;                                                                     {% ?? bvrs_has_deletion %}
  """
)

lvi_body_props_tpl = chop0(
    """
isSelected: boolean;                                                                    {% ?? bvrs_has_selection %}
isHighlighted: boolean;                                                                 {% ?? bvrs_has_selection %}
dragState?: string;                                                                     {% ?? bvrs_has_drag_and_drop %}
  """
)

lvi_body_additional_props_tpl = chop0(
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
{% end_magic_with %}
  """
)
