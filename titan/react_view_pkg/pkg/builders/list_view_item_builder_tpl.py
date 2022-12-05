from moonleap.utils import chop0

lvi_fields_tpl = chop0(
    """
{% magic_with _.component.item_name as myItemName %}
{% magic_with field_spec.name as fieldSpecName %}
        <div>                                                                                       {% for field_spec in __.fields %}{% if field_spec.display %}
          {props.myItemName.fieldSpecName}                                                          {% ?? field_spec.field_type not in ("boolean",) %}
          fieldSpecName: {props.myItemName.fieldSpecName ? 'Yes' : 'No'}                            {% ?? field_spec.field_type in ("boolean",) %}
        </div>                                                                                      {% endif %}{% endfor %}
{% end_magic_with %}
{% end_magic_with %}
"""
)

lvi_buttons_tpl = chop0(
    """
        <div                                                                                          {% if __.deletion_bvr %}
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
        </div>                                                                                        {% endif %}
    """
)

lvi_styles_tpl = chop0(
  """
{% magic_with component_name as MyComponent %}
{                                                                                           {% min_lines count=3 %}
  'MyComponent--selected': props.isSelected,                                                {% ?? selection_bvr %}
  'MyComponent--highlighted': props.isHighlighted,                                          {% ?? highlight_bvr %}
},                                                                                          {% end_min_lines %}
`MyComponent--drag-${props.dragState}`                                                      {% ?? drag_and_drop_bvr %}
{% end_magic_with %}
  """

lvi_props_tpl = chop0(
  """
{% magic_with component_name as MyComponent %}
{...clickHandlers(props)}                                                                   {% ?? selection_bvr %}
{...dragHandlers(props)}                                                                    {% ?? drag_and_drop_bvr %}
{% end_magic_with %}
  """

lvi_buttons_imports_tpl = chop0(
  """
import { smallButton } from 'src/frames/components';
  """

lvi_body_imports_tpl = chop0(
  """
import { dragHandlers, type DragHandlersT } from 'skandha-facets/DragAndDrop';                      {% ?? __.drag_and_drop_bvr %}
import { clickHandlers, ClickHandlersT } from 'skandha-facets/handlers/ClickToSelectItems';         {% ?? __.selection_bvr %}
  """

lvi_buttons_props_tpl = chop0(
  """
onDelete: Function;                                                                               {% ?? __.deletion_bvr %}
  """

lvi_body_props_tpl = chop0(
  """
isSelected: boolean;                                                                              {% ?? __.selection_bvr %}
isHighlighted: boolean;                                                                           {% ?? __.selection_bvr %}
dragState?: string;                                                                               {% ?? __.drag_and_drop_bvr %}
  """

lvi_body_additional_props_tpl = chop0(
  """
& ClickHandlersT                                                                                    {% ?? __.selection_bvr %}
& DragHandlersT                                                                                     {% ?? __.drag_and_drop_bvr %}
  """

lvi_buttons_preamble_tpl = chop0(
  """
{% magic_with item_name as myItemName %}
if (isUpdating(props.myItemName)) {
  return UIkit && <div data-uk-spinner className=""></div>;                                     {% ?? uikit %}
  return null;                                                                                  {% ?? not uikit %}
}
{% end_magic_with %}
  """
