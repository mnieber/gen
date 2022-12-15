from moonleap import Tpls, chop0
from moonleap.utils.fp import append_uniq, extend_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin


class ListViewBuilder(Builder, BvrsBuilderMixin):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)

    def get_spec_extension(self, places):
        named_item_term_str = self.widget_spec.get_value_by_name("items").removesuffix(
            "~list"
        )
        lvi_name = lvi_name = (
            self.widget_spec.get_value_by_name("lvi-name")
            or self._get_default_lvi_name()
        )

        result = {}
        if "ListViewItem" not in places:
            result.update(lvi_spec(lvi_name))
        if "LviComponent" not in places:
            result.update(lvi_component_spec(lvi_name, named_item_term_str))
        return result

    def _get_default_lvi_name(self):
        default_lvi_name = self.widget_spec.root.widget_name
        if "-:" in default_lvi_name:
            default_lvi_name = default_lvi_name.replace("-:", "-") + "-item:view"
        else:
            pos = default_lvi_name.find(":")
            default_lvi_name = default_lvi_name[:pos] + "-item:view"
        return default_lvi_name

    def build(self):
        self._add_default_props()
        self._add_lines()

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_default_props())

    def _get_context(self):
        return {
            **self.bvrs_context(),
            "item_name": self.bvrs_item_name,
            "items_expr": self.item_list_data_path(),
            "component_name": self.widget_spec.widget_class_name,
        }

    def _add_lines(self):
        context = self._get_context()
        context["child_widget_div"] = self.output.graft(
            _get_lvi_instance_output(
                self.widget_spec,
                div_attrs=tpls.render("list_view_lvi_props_tpl", context),
                key=f"{self.bvrs_item_name}.id",
            )
        )

        self.add(
            imports_lines=[tpls.render("list_view_imports_tpl", context)],
            preamble_hooks_lines=[tpls.render("list_view_preamble_hooks_tpl", context)],
            preamble_lines=[tpls.render("list_view_preamble_tpl", context)],
            lines=[tpls.render("list_view_lvi_instance_tpl", context)],
        )


def lvi_spec(lvi_name):
    return {
        f"ListViewItem with {lvi_name}": "pass",
    }


def lvi_component_spec(lvi_name, named_item_term_str):
    return {
        f"LviComponent with {lvi_name} as ListViewItem, Bar[p-2]": {
            "__default_props__": [named_item_term_str],
            "LeftSlot with ItemFields": "display=1",
            "RightSlot with Buttons as LviButtons": "pass",
        },
    }


def _get_lvi_instance_output(widget_spec, div_attrs, key):
    # This returns the div that is used in the ListView.
    # Don't confuse this with the div that is used in the ListViewItem.
    from titan.react_view_pkg.pkg.build import build

    child_widget_spec = widget_spec.find_child_with_place("ListViewItem")
    with child_widget_spec.memo():
        child_widget_spec.div.key = key
        if div_attrs:
            append_uniq(child_widget_spec.div.attrs, div_attrs)
        return build(child_widget_spec)


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
{% magic_with item_name as myItem %}
const dragAndDropUIConnector = useDragAndDropUIConnector(                                     {% if bvrs_has_drag_and_drop %}
    props.myItemsDragAndDrop
);                                                                                            {% endif %}
const selectionUIConnector = useSelectionUIConnector(props.myItemsSelection);                 {% ?? bvrs_has_selection %}
{{ "" }}
{% end_magic_with %}
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
