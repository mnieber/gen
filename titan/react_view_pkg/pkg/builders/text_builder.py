from titan.react_view_pkg.pkg.builder import Builder


class TextBuilder(Builder):
    def build(self, classes=None, handlers=None):
        value = self.widget_spec.values["value"]
        self.add_lines(
            [f'<div className={{cn("{self.output.widget_class_name}")}}>{value}</div>']
        )
