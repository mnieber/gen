from titan.react_view_pkg.pkg.builder import Builder


class EmptyBuilder(Builder):
    def build(self, div_attrs=None):
        self._add_div_open(div_attrs)
        self._add_div_close()
