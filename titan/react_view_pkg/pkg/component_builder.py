from titan.react_view_pkg.pkg.builder import Builder


class ComponentBuilder(Builder):
    def build(self, classes=None):
        self += [f"<{self.output.widget_name} />"]
