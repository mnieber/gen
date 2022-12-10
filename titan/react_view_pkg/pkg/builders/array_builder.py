from moonleap import Tpls, u0
from moonleap.utils import chop0
from moonleap.utils.inflect import singular
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

tpls = Tpls("array_builder", preamble_tpl=preamble_tpl, instance_tpl=instance_tpl)


class ArrayBuilder(Builder):
    def build(self):
        item_name = self.named_item_list_term.data

        const_name = self.widget_spec.widget_name
        child_widget_div = self.output.graft(
            _get_child_widget_output(
                self.widget_spec,
                item_name,
                class_name=f"{self.widget_spec.parent_ws.widget_class_name}"
                + f"__{u0(singular(const_name))}",
            )
        )
        context = {
            "const_name": const_name,
            "items_expr": self.item_list_data_path(),
            "item_name": item_name,
            "child_widget_div": child_widget_div,
        }

        self.add(
            preamble_lines=[tpls.render("preamble_tpl", context)],
            lines=[tpls.render("instance_tpl", context)],
        )


def _get_child_widget_output(widget_spec, item_name, class_name):
    from titan.react_view_pkg.pkg.build import build

    child_widget_spec = widget_spec.find_child_with_place("Child")
    with child_widget_spec.memo():
        child_widget_spec.set_widget_class_name(class_name)
        child_widget_spec.values["item"] = item_name
        child_widget_spec.div_key = f"{item_name}.id"
        return build(child_widget_spec)
