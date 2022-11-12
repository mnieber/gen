from titan.react_view_pkg.pkg.builder import Builder


class ComponentBuilder(Builder):
    def get_div(self, classes=None):
        self += [f"<{self.widget_name} />"]
        return self._output()
