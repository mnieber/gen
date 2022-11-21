from titan.react_view_pkg.pkg.builder import Builder


class EmptyBuilder(Builder):
    def build(self, classes=None, handlers=None):
        self._add_div_open(classes or [], handlers)
        self._add_div_close()
