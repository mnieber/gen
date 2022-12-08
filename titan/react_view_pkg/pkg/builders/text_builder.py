from titan.react_view_pkg.pkg.builder import Builder


class TextBuilder(Builder):
    def build(self):
        value = self.widget_spec.values["value"]
        self.add(
            lines=[
                f'<div className={{cn("{self.widget_spec.widget_class_name}")}}>{value}</div>'
            ]
        )
