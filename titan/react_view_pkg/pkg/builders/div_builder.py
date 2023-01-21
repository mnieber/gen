from titan.react_view_pkg.pkg.builder import Builder


class DivBuilder(Builder):
    type = "Div"

    def build(self):
        self._add_div_open()
        self._add_child_widgets()
        self._add_div_close()
