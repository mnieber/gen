from moonleap.utils import chop0
from moonleap.utils.fp import extend_uniq
from moonleap.utils.inflect import plural
from titan.react_view_pkg.pkg.builder import Builder


def default_spec(item_name):
    lvi_name = f"{ item_name }-list-view-item:view"
    # TODO: use lvi_name
    return {f"ListViewItem with Card": {"ItemFields[cn=__]": "pass"}}


imports_tpl = chop0(
    """
{% magic_with item_name as myItem %}
import { MyItemT } from 'src/api/types/MyItemT';
import { ClickToSelectItems } from 'skandha-facets/handlers';                                 {% ?? selection_bvr %}
import { dragState } from 'skandha-facets/DragAndDrop';                                       {% ?? drag_and_drop_bvr %}
{% end_magic_with %}
"""
)

preamble_tpl = chop0(
    """
{% magic_with item_name as myItem %}
const handleClick = new ClickToSelectItems({                                                  {% if selection_bvr %}
    selection: props.myItemsSelection
});
                                                                                              {% endif %}
const noItems = <h2>There are no myItems</h2>;

const myItemDivs = {{ items_expr }}.map(({{ item_name }}: {{ item_name|u0 }}T) => {
  {{ child_widget_div }}
});

{% end_magic_with %}
"""
)

props_tpl = chop0(
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

instance_tpl = chop0(
    """
{% magic_with item_name as myItem %}
{myItemDivs.length > 0 && myItemDivs}
{myItemDivs.length === 0 && noItems}
{% end_magic_with %}
"""
)


class ListViewBuilder(Builder):
    def build(self):
        __import__("pudb").set_trace()
        item_name = self.item_list.item.item_name
        items_name = plural(item_name)
        bvrs = self.widget_spec.values.get("bvrs", []).split(",")

        has_selection = "selection" in bvrs
        has_highlight = "highlight" in bvrs
        has_drag_and_drop = "dragAndDrop" in bvrs
        has_deletion = "deletion" in bvrs

        extend_uniq(
            self.output.default_props,
            []
            + ([f"{items_name}:selection"] if has_selection else [])
            + ([f"{items_name}:highlight"] if has_highlight else [])
            + ([f"{items_name}:drag-and-drop"] if has_drag_and_drop else [])
            + ([f"{items_name}:deletion"] if has_deletion else []),
        )

        context = {
            "item_name": item_name,
            "items_expr": self.item_list_data_path(),
            "selection_bvr": has_selection,
            "highlight_bvr": has_highlight,
            "drag_and_drop_bvr": has_drag_and_drop,
            "deletion_bvr": has_deletion,
        }

        if True:
            code = self.render_str(imports_tpl, context, "list_view_builder_imports.j2")
            self.add_import_lines([code])

        if True:
            code = self.render_str(
                instance_tpl, context, "list_view_builder_instance.j2"
            )
            self.add_lines([code])

        if True:
            props = self.render_str(props_tpl, context, "list_view_builder_props.j2")
            context["child_widget_div"] = self._get_child_widget_div(props, item_name)
            code = self.render_str(
                preamble_tpl, context, "list_view_builder_preamble.j2"
            )
            self.add_preamble_lines([code])

    def _get_child_widget_div(self, props, item_name):
        from titan.react_view_pkg.pkg.get_builder import get_builder

        child_widget_spec = self.get_or_create_place_widget_spec(
            "ListViewItem", default_spec(item_name)
        )
        memo = child_widget_spec.create_memo()
        # TODO: this is a bit weird. How to tell the generator to use the right item?
        child_widget_spec.values["item"] = f"+{item_name}:item"
        child_widget_spec.div_key = f"{item_name}.id"
        child_widget_spec.div_props += [props]
        builder = get_builder(child_widget_spec, parent_builder=self)
        builder.build()
        child_widget_spec.restore_memo(memo)
        return builder.output.div
