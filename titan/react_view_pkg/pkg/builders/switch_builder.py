from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.builder import Builder


class SwitchBuilder(Builder):
    type = "Switch"

    def build(self):
        cond = self.get_value("cond")
        if not self.widget_spec.is_component_def:
            self.output.add(
                lines=[
                    "{/*              */}",
                    "{/* 🟩 Switch 🟩 */}",
                    "{/*              */}",
                ]
            )
        self.output.add(lines=[f"{{{cond} &&"])
        add_child_widgets(self, [self.widget_spec.child_widget_specs[0]])
        self.output.add(lines=[f"}}"])
        self.output.add(lines=[f"{{!{cond} &&"])
        add_child_widgets(self, [self.widget_spec.child_widget_specs[1]])
        self.output.add(lines=[f"}}"])
