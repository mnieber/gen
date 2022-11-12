from titan.react_view_pkg.pkg.builder import Builder


class BarBuilder(Builder):
    def get_div(self, classes=None):
        self._add_div_open((classes or []) + ['"self-center"'])
        self._add_child_widgets()
        return self._add_div_close()
