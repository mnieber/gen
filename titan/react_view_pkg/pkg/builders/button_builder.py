from moonleap import Tpls
from titan.react_view_pkg.pkg.builder import Builder


class ButtonBuilder(Builder):
    def update_widget_spec(self):
        handler = (
            self.widget_spec.values.get("handler")
            or '() => console.log("Moonleap Todo")'
        )
        self.widget_spec.div.attrs += [f"onClick={{ {handler} }}"]


tpls = Tpls(
    "button_builder",
)
