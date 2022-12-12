from titan.react_view_pkg.pkg.builder import Builder

from .button_builder_tpl import tpls


class ButtonBuilder(Builder):
    def build(self):
        title = self.widget_spec.values["title"]
        handler = self.widget_spec.values.get("handler", None)

        context = {
            "title": title,
            "class_name": self.widget_spec.widget_class_name,
            "handler": handler or "() => { console.log('Moonleap Todo'); }",
        }
        self.add(lines=[tpls.render("button_div_tpl", context)])
