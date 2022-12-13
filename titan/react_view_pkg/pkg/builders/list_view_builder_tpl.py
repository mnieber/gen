from moonleap import Tpls, chop0

list_view_imports_tpl = chop0(
    """
{% magic_with item_name as myItem %}
import { MyItemT } from 'src/api/types/MyItemT';
import {
    useSelectionUIConnector,                                                                  {% ?? bvrs_has_selection %}
    useDragAndDropUIConnector,                                                                {% ?? bvrs_has_drag_and_drop %}
} from 'skandha-mobx/hooks';
{% end_magic_with %}
"""
)

list_view_preamble_hooks_tpl = chop0(
    """
const dragAndDropUIConnector = useDragAndDropUIConnector(                                     {% if bvrs_has_drag_and_drop %}
    props.myItemsDragAndDrop
);                                                                                            {% endif %}
const selectionUIConnector = useSelectionUIConnector(props.myItemsSelection);                 {% ?? bvrs_has_selection %}
{{ "" }}
"""
)

list_view_preamble_tpl = chop0(
    """
{% magic_with item_name as myItem %}
const noItems = <h2>There are no myItems</h2>;

const myItemDivs = {{ items_expr }}.map(({{ item_name }}: {{ item_name|u0 }}T) => {
  {{ child_widget_div }}
});
{{ "" }}
{% end_magic_with %}
"""
)

list_view_lvi_props_tpl = chop0(
    """
{% magic_with item_name as myItem %}
myItem={myItem}
isHighlighted={myItem && props.myItemsHighlight.id === myItem.id}                             {% ?? bvrs_has_highlight %}
onDelete={() => props.myItemsDeletion.delete([myItem.id])}                                    {% ?? bvrs_has_deletion %}
selectionUIProps={selectionUIConnector.handle(myItem.id)}                                     {% ?? bvrs_has_selection %}
dragAndDropUIProps={dragAndDropUIConnector.handle(myItem.id)}                                 {% ?? bvrs_has_drag_and_drop %}
{% end_magic_with %}
"""
)

list_view_lvi_instance_tpl = chop0(
    """
{% magic_with item_name as myItem %}
{myItemDivs.length > 0 && myItemDivs}
{myItemDivs.length === 0 && noItems}
{% end_magic_with %}
"""
)

tpls = Tpls(
    "list_view_builder",
    list_view_imports_tpl=list_view_imports_tpl,
    list_view_preamble_hooks_tpl=list_view_preamble_hooks_tpl,
    list_view_preamble_tpl=list_view_preamble_tpl,
    list_view_lvi_props_tpl=list_view_lvi_props_tpl,
    list_view_lvi_instance_tpl=list_view_lvi_instance_tpl,
)
