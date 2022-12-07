from moonleap.utils import chop0

lvi_imports_tpl = chop0(
    """
{% magic_with item_name as myItem %}
import { MyItemT } from 'src/api/types/MyItemT';
import { ClickToSelectItems } from 'skandha-facets/handlers';                                 {% ?? bvrs_has_selection %}
import { dragState } from 'skandha-facets/DragAndDrop';                                       {% ?? bvrs_has_drag_and_drop %}
{% end_magic_with %}
"""
)

lvi_preamble_tpl = chop0(
    """
{% magic_with item_name as myItem %}
const handleClick = new ClickToSelectItems({                                                  {% if bvrs_has_selection %}
    selection: props.myItemsSelection
});
{{ "" }}                                                                                      {% endif %}
const noItems = <h2>There are no myItems</h2>;

const myItemDivs = {{ items_expr }}.map(({{ item_name }}: {{ item_name|u0 }}T) => {
  {{ child_widget_div }}
});
{{ "" }}
{% end_magic_with %}
"""
)

lvi_instance_props_tpl = chop0(
    """
{% magic_with item_name as myItem %}
myItem={myItem}
isSelected={myItem && props.myItemsSelection.ids.includes(myItem.id)}                         {% ?? bvrs_has_selection %}
isHighlighted={myItem && props.myItemsHighlight.id === myItem.id}                             {% ?? bvrs_has_highlight %}
dragState={dragState(props.myItemsDragAndDrop.hoverPosition, myItem.id)}                      {% ?? bvrs_has_drag_and_drop %}
onDelete={() => props.myItemsDeletion.delete([myItem.id])}                                    {% ?? bvrs_has_deletion %}
{...handleClick.handle(myItem.id)}                                                            {% ?? bvrs_has_selection %}
{...props.myItemsDragAndDrop.handle(myItem.id)}                                               {% ?? bvrs_has_drag_and_drop %}
{% end_magic_with %}
"""
)

lvi_instance_tpl = chop0(
    """
{% magic_with item_name as myItem %}
{myItemDivs.length > 0 && myItemDivs}
{myItemDivs.length === 0 && noItems}
{% end_magic_with %}
"""
)

lvi_body_div_styles_tpl = chop0(
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

lvi_body_div_attrs_tpl = chop0(
    """
{...clickHandlers(props)}                                                               {% ?? bvrs_has_selection %}
{...dragHandlers(props)}                                                                {% ?? bvrs_has_drag_and_drop %}
  """
)
