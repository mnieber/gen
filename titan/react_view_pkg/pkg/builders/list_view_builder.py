from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.verbatim_builder import VerbatimBuilder

view_div = chop0(
    """
{myItemDivs.length > 0 && myItemDivs}
{myItemDivs.length === 0 && noItems}"""
)


class ListViewBuilder(Builder):
    def __init__(self, widget_spec, parent_builder, level, list_view):
        super().__init__(widget_spec, parent_builder, level)
        self.list_view = list_view
        self._register_builders()

    def _register_builders(self):
        self.register_builder_type("ListViewItems", self._get_list_view_items)

    def _get_list_view_items(self, *args, **kwargs):
        div = view_div.replace("myItem", self.list_view.item_name)
        return VerbatimBuilder(*args, **kwargs, div=div)

    def build(self, div_attrs=None):
        self.widget_spec.remove_child_with_place("ListViewItem")
        inner_builder = get_child_widget_builder(self, self.widget_spec, self.level)

        inner_builder.build(div_attrs)
        self.output.add(inner_builder.output)
