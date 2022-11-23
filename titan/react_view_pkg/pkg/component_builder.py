from titan.react_view_pkg.pkg.builder import Builder


class ComponentBuilder(Builder):
    def build(self, classes=None, handlers=None):
        self.add_lines([f"<{self.output.widget_class_name} />"])
