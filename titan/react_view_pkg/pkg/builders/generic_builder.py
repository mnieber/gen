from titan.react_view_pkg.pkg.builder import Builder


class GenericBuilder(Builder):
    type = "Generic"

    def build(self):
        if self.widget_spec.is_component_def and not self.widget_spec.has_tag(
            "no_scss"
        ):
            self.widget_spec.div.append_styles(["props.className"])

        if self.get_value("banner") == "1":
            self.output.add(lines=[tpl_banner(self.widget_spec.widget_name)])

    def update_widget_spec(self):
        if "Children" in self.widget_spec.widget_base_types:
            self.widget_spec.root.add_tag("has_children_prop")

        if self.get_value("noScss"):
            self.widget_spec.add_tag("no_scss")

        if tabIndex := self.get_value("tabIndex"):
            self.widget_spec.div.append_attrs([f"tabIndex={tabIndex}"])


def tpl_banner(name):
    white_space = " " * (len(name) + 6)
    open = "{"
    close = "}"

    return f"""
    {open}/* {white_space} */{close}
    {open}/* 🟩 {name} 🟩 */{close}
    {open}/* {white_space} */{close}"""
