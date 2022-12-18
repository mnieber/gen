from titan.react_view_pkg.pkg.builder import Builder


class IconBuilder(Builder):
    def build(self):
        name = self.widget_spec.values["name"]
        self.output.add_react_package("frames", f"icons/{name}Icon", "icons")
