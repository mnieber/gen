from moonleap.render.template_env import get_template_from_str
from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder

template_str = chop0(
    """
const {{ const_name }} = {{ items_expr }}.map(({{ item }}: {{ item|u0 }}T) => {
  {{ child_widget_div }}
});
"""
)


class ArrayBuilder(Builder):
    def __post_init__(self):
        self.const_name = self.widget_spec.widget_name
        self.item_name = self.item_list.item.item_name
        self.div = f"{{{self.const_name}}}"

    def build(self):
        code = get_template_from_str(template_str).render(
            {
                "const_name": self.const_name,
                "items_expr": self.item_list_data_path(),
                "item": self.item_name,
                "child_widget_div": self._get_child_widget_div(),
            }
        )
        self.output.preamble_lines.extend([code])
        self.add_lines([self.div])

    def _get_child_widget_div(self):
        child_widget_spec = self.widget_spec.find_child_with_place("Child")
        child_widget_spec.div_key = f"{self.item_name}.id"
        child_widget_spec.builder.build()
        return child_widget_spec.builder.output.div
