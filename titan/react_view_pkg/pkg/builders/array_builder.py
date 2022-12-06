from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder

preamble_tpl = chop0(
    """
const {{ const_name }} = {{ items_expr }}.map(({{ item_name }}: {{ item_name|u0 }}T) => {
  {{ child_widget_div }}
});
"""
)

instance_tpl = chop0(
    """
{ {{ const_name }} }
"""
)


class ArrayBuilder(Builder):
    def build(self):
        item_name = self.item_list.item.item_name

        context = {
            "const_name": self.widget_spec.widget_name,
            "items_expr": self.item_list_data_path(),
            "item_name": item_name,
            "child_widget_div": _get_child_widget_div(self.widget_spec, item_name),
        }

        if True:
            code = self.render_str(preamble_tpl, context, "array_builder_preamble.j2")
            self.add_preamble_lines([code])

        if True:
            code = self.render_str(instance_tpl, context, "array_builder_instance.j2")
            self.add_lines([code])


def _get_child_widget_div(widget_spec, item_name):
    from titan.react_view_pkg.pkg.get_builder import get_builder

    child_widget_spec = widget_spec.find_child_with_place("Child")
    memo = child_widget_spec.create_memo()
    child_widget_spec.values["item"] = item_name
    child_widget_spec.div_key = f"{item_name}.id"
    builder = get_builder(child_widget_spec)
    builder.build()
    child_widget_spec.restore_memo(memo)
    return builder.output.div
