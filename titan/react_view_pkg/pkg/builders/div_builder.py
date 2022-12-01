from titan.react_view_pkg.pkg.builder import Builder


class DivBuilder(Builder):
    def build(self, div_attrs=None):
        self._add_div_open(div_attrs)
        self._add_child_widgets()
        self._add_div_close()
