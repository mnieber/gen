from titan.react_view_pkg.pkg.builder import Builder


class DivBuilder(Builder):
    def build(self, classes=None):
        self._add_div_open((classes or []))
        self._add_child_widgets()
        self._add_div_close()
