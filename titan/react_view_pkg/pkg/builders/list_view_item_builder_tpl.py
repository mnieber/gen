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

lvi_imports_tpl = chop0(
    """
import { dragHandlers, type DragHandlersT } from 'skandha-facets/DragAndDrop';                      {% ?? bvrs_has_drag_and_drop %}
import { clickHandlers, ClickHandlersT } from 'skandha-facets/handlers/ClickToSelectItems';         {% ?? bvrs_has_selection %}
  """
)

lvi_props_tpl = chop0(
    """
isSelected: boolean;                                                                    {% ?? bvrs_has_selection %}
isHighlighted: boolean;                                                                 {% ?? bvrs_has_selection %}
dragState?: string;                                                                     {% ?? bvrs_has_drag_and_drop %}
  """
)

lvi_div_attrs_tpl = chop0(
    """
{...clickHandlers(props)}                                                               {% ?? bvrs_has_selection %}
{...dragHandlers(props)}                                                                {% ?? bvrs_has_drag_and_drop %}
  """
)

lvi_div_styles_tpl = chop0(
    """
{% magic_with component_name as MyComponent %}
{                                                                                       {% min_lines count=3 %}
  'MyComponent--selected': props.isSelected,                                            {% ?? bvrs_has_selection %}
  'MyComponent--highlighted': props.isHighlighted,                                      {% ?? bvrs_has_highlight %}
},                                                                                      {% end_min_lines %}
`MyComponent--drag-${props.dragState}`                                                  {% ?? bvrs_has_drag_and_drop %}
{% end_magic_with %}
  """
)
