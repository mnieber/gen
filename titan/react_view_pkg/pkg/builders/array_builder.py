from moonleap.render.template_env import get_template_from_str
from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder

template_str = chop0(
    """
const {{ widget_name }} = {{ items_expr }}.map((section: SectionT) => {
  return (
    <div key={section.id} section={section}>
      Moonleap Todo
    </div>
  );
});
"""
)


class ArrayBuilder(Builder):
    def build(self, classes=None, handlers=None):
        child_slot = self.widget_spec.find_child_with_place("Child")
        component = self.widget_spec.component

        t = get_template_from_str(template_str)
        code = t.render(
            {
                "widget_name": self.widget_spec.widget_name,
                "items_expr": "props.page.sections" or self.widget_spec.values["items"],
            }
        )
        self.output.preamble_lines.extend([code])
        self.add_lines(["{%s}" % self.widget_spec.widget_name])
