from moonleap.render.template_env import get_template_from_str
from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builder_items_mixin import BuilderItemsMixin
from titan.react_view_pkg.pkg.div_attrs import update_div_attrs

template_str = chop0(
    """
const {{ const_name }} = {{ items_expr }}.map(({{ item }}: {{ item|u0 }}T) => {
  {{ child_widget_div }}
});
"""
)


class ArrayBuilder(BuilderItemsMixin, Builder):
    def build(self, div_attrs=None):
        const_name = self.widget_spec.widget_name
        item_name = self.item_list.item.item_name
        code = get_template_from_str(template_str).render(
            {
                "const_name": const_name,
                "items_expr": self.item_list_expr(),
                "item": item_name,
                "child_widget_div": self._get_child_widget_div(
                    update_div_attrs(div_attrs, key=f"{item_name}.id")
                ),
            }
        )
        self.output.preamble_lines.extend([code])
        self.add_lines([f"{{{const_name}}}"])

    def _get_child_widget_div(self, div_attrs):
        from titan.react_view_pkg.pkg.get_builder import get_builder

        child_widget_spec = self.widget_spec.find_child_with_place("Child")
        child_builder = get_builder(child_widget_spec, self, self.level + 1)
        child_builder.build(div_attrs)
        child_widget_div = child_builder.output.div
        return child_widget_div
