from titan.react_view_pkg.pkg.builder import Builder


class TextBuilder(Builder):
    def build(self):
        text = self.widget_spec.values["text"]
        self.output.add(lines=[f"{text}"])
