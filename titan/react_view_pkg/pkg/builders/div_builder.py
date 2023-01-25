from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.add_div import add_div_close, add_div_open
from titan.react_view_pkg.pkg.builder import Builder


class DivBuilder(Builder):
    type = "Div"

    def build(self):
        add_div_open(self)
        self.add_body()
        add_div_close(self)

    def add_body(self):
        add_child_widgets(self, self.widget_spec.child_widget_specs)
