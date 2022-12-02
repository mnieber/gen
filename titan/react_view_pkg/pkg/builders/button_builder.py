from moonleap.render.template_env import get_template_from_str
from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder

handler_template_str = chop0(
    """
    const {{ handler }} = () => {
        console.log("Moonleap Todo");
    };

"""
)

button_template_str = chop0(
    """
    <div
      className={cn("{{ class_name }}", "button")}
      onClick={ {{ handler }} }
    >
      {{ title }}
    </div>
"""
)


class ButtonBuilder(Builder):
    def build(self, div_attrs):
        title = self.widget_spec.values["title"]
        handler = self.widget_spec.values.get("handler", None)
        self.output.external_css_classes += ["button"]

        if handler:
            code = get_template_from_str(handler_template_str).render(
                {
                    "handler": handler,
                }
            )
            self.add_preamble([code])

        code = get_template_from_str(button_template_str).render(
            {
                "title": title,
                "class_name": self.widget_spec.widget_name,
                "handler": handler or "() => { console.log('Moonleap Todo'); }",
            }
        )
        self.add_lines([code])
