from titan.react_view_pkg.pkg.builder import Builder


class GenericBuilder(Builder):
    type = "Generic"

    def update_widget_spec(self):
        if self.get_value("noScss"):
            self.widget_spec.add_tag("no_scss")
