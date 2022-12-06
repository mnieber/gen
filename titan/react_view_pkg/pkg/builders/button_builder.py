from titan.react_view_pkg.pkg.builder import Builder

from .button_builder_tpl import button_div_tpl, button_handler_tpl


class ButtonBuilder(Builder):
    def build(self):
        title = self.widget_spec.values["title"]
        handler = self.widget_spec.values.get("handler", None)

        # Handler
        if handler:
            context = {
                "handler": handler,
            }
            code = self.render_str(
                button_handler_tpl, context, "button_builder_handler.j2"
            )
            self.add_preamble_lines([code])

        # Div
        if True:
            context = {
                "title": title,
                "class_name": self.widget_spec.widget_name,
                "handler": handler or "() => { console.log('Moonleap Todo'); }",
            }
            code = self.render_str(button_div_tpl, context, "button_builder_button.j2")
            self.add_lines([code])
