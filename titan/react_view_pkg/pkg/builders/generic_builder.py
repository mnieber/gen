from titan.react_view_pkg.pkg.builder import Builder


class GenericBuilder(Builder):
    type = "Generic"

    def build(self):
        if self.widget_spec.is_component_def and not self.widget_spec.has_tag(
            "no_scss"
        ):
            self.widget_spec.div.append_styles(["props.className"])

    def update_widget_spec(self):
        if "Children" in self.widget_spec.widget_base_types:
            self.widget_spec.root.add_tag("has_children_prop")

        if self.get_value("noScss"):
            self.widget_spec.add_tag("no_scss")
