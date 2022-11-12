from titan.react_view_pkg.pkg.builder import Builder


class CardBuilder(Builder):
    def get_div(self, classes=None):
        self._add_div_open((classes or []) + ["card"])
        self._add_child_widgets()
        return self._add_div_close()
