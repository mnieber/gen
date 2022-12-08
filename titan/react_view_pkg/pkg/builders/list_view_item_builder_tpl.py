from moonleap.utils import chop0

lvi_imports_tpl = chop0(
    """
import {                                                                                {% if bvrs_has_drag_and_drop %}
  dragAndDropUIHandlers,
  DragAndDropUIPropsT,
} from 'skandha-facets/DragAndDrop';                                                    {% endif %}
import {                                                                                {% if bvrs_has_selection %}
  selectionUIHandlers,
  SelectionUIPropsT,
} from 'skandha-facets/Selection';                                                      {% endif %}
  """
)

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

lvi_props_tpl = chop0(
    """
isHighlighted: boolean;                                                                 {% ?? bvrs_has_selection %}
dragAndDropUIProps: DragAndDropUIPropsT;                                                {% ?? bvrs_has_drag_and_drop %}
selectionUIProps: SelectionUIPropsT;                                                    {% ?? bvrs_has_selection %}
  """
)

lvi_div_attrs_tpl = chop0(
    """
{...selectionUIHandlers(props.selectionUIProps)}                                        {% ?? bvrs_has_selection %}
{...dragAndDropUIHandlers(props.dragAndDropUIProps)}                                    {% ?? bvrs_has_drag_and_drop %}
  """
)

lvi_div_styles_tpl = chop0(
    """
{% magic_with component_name as MyComponent %}
{                                                                                       {% min_lines count=3 %}
  'MyComponent--selected': props.selectionUIProps.isSelected,                           {% ?? bvrs_has_selection %}
  'MyComponent--highlighted': props.isHighlighted,                                      {% ?? bvrs_has_highlight %}
},                                                                                      {% end_min_lines %}
`MyComponent--drag-${props.dragAndDropUIProps.dragState}`                               {% ?? bvrs_has_drag_and_drop %}
{% end_magic_with %}
  """
)
