from titan.react_view_pkg.pkg.builder import Builder


class TextBuilder(Builder):
    def build(self):
        value = self.widget_spec.values["value"]
        self.output.add(lines=[f"{value}"])
