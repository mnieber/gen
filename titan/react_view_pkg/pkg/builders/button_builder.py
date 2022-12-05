from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder

handler_tpl = chop0(
    """
    const {{ handler }} = () => {
        console.log("Moonleap Todo");
    };

"""
)

button_tpl = chop0(
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
    def build(self):
        title = self.widget_spec.values["title"]
        handler = self.widget_spec.values.get("handler", None)
        self.output.external_css_classes += ["button"]

        if handler:
            context = {
                "handler": handler,
            }
            code = self.render_str(handler_tpl, context, "button_builder_handler.j2")
            self.add_preamble_lines([code])

        if True:
            context = {
                "title": title,
                "class_name": self.widget_spec.widget_name,
                "handler": handler or "() => { console.log('Moonleap Todo'); }",
            }
            code = self.render_str(button_tpl, context, "button_builder_button.j2")
            self.add_lines([code])
