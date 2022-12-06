from moonleap.utils import chop0

lvi_imports_tpl = chop0(
    """
{% magic_with item_name as myItem %}
import { MyItemT } from 'src/api/types/MyItemT';
import { ClickToSelectItems } from 'skandha-facets/handlers';                                 {% ?? selection_bvr %}
import { dragState } from 'skandha-facets/DragAndDrop';                                       {% ?? drag_and_drop_bvr %}
{% end_magic_with %}
"""
)

lvi_preamble_tpl = chop0(
    """
{% magic_with item_name as myItem %}
const handleClick = new ClickToSelectItems({                                                  {% if selection_bvr %}
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
isSelected={myItem && props.myItemsSelection.ids.includes(myItem.id)}                         {% ?? selection_bvr %}
isHighlighted={myItem && props.myItemsHighlight.id === myItem.id}                             {% ?? highlight_bvr %}
dragState={dragState(props.myItemsDragAndDrop.hoverPosition, myItem.id)}                      {% ?? drag_and_drop_bvr %}
onDelete={() => props.myItemsDeletion.delete([myItem.id])}                                    {% ?? deletion_bvr %}
{...handleClick.handle(myItem.id)}                                                            {% ?? selection_bvr %}
{...props.myItemsDragAndDrop.handle(myItem.id)}                                               {% ?? drag_and_drop_bvr %}
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
