from moonleap import Tpls
from titan.react_view_pkg.pkg.builder import Builder


class ButtonBuilder(Builder):
    def update_widget_spec(self):
        self.widget_spec.div_attrs += ['onClick={() => console.log("Moonleap Todo")}']


tpls = Tpls(
    "button_builder",
)
