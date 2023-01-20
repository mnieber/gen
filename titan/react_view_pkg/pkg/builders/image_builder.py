from titan.react_view_pkg.pkg.builder import Builder


class ImageBuilder(Builder):
    def build(self):
        url = self.widget_spec.values["url"]
        self.output.add(lines=[f"{url}"])
