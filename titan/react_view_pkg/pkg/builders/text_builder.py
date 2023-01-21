from titan.react_view_pkg.pkg.builder import Builder


class TextBuilder(Builder):
    type = "Text"

    def build(self):
        text = self.get_value("text")
        self.output.add(lines=[f"{text}"])
