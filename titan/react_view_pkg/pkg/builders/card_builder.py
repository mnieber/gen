from titan.react_view_pkg.pkg.builder import Builder


class CardBuilder(Builder):
    def build(self, classes=None, handlers=None):
        self._add_div_open(["card"] + (classes or []), handlers)
        self._add_child_widgets()
        self._add_div_close()
