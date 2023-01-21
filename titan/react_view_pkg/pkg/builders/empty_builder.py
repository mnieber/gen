from titan.react_view_pkg.pkg.builder import Builder


class EmptyBuilder(Builder):
    type = "Empty"

    def build(self):
        self._add_div_open()
        self._add_div_close()
