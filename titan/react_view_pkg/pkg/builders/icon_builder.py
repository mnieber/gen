from titan.react_view_pkg.pkg.builder import Builder


class IconBuilder(Builder):
    def build(self):
        name = self.widget_spec.values["name"]
        self.output.set_flags([f"frames/{name}Icon"])
