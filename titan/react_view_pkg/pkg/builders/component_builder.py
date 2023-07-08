from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.form_state_provider_builder.form_state_provider_builder import (
    get_url_state_default_prop,
)
from titan.widgetspec.create_widget_class_name import get_component_name


class ComponentBuilder(Builder):
    @property
    def has_child_widgets(self):
        return bool(self.widget_spec.child_widget_specs)

    def build(self):
        self.url_state = get_url_state_default_prop(self.widget_spec)
        self.add_div_open()
        self.add_body()
        self.add_div_close()

    def add_div_open(self):
        if self.has_child_widgets:
            self.output.add(
                lines=[f"<{self.widget_spec.widget_class_name}>"],
            )
        else:
            self.output.add(
                lines=[f"<{self.widget_spec.widget_class_name}/>"],
            )

    def add_body(self):
        parent_module_name = (
            self.widget_spec.parent.module_name if self.widget_spec.parent else None
        )
        self.output.add(
            imports=[_get_component_import_path(self.widget_spec, parent_module_name)]
        )
        add_child_widgets(self, self.widget_spec.child_widget_specs)

    def add_div_close(self):
        if self.has_child_widgets:
            self.output.add(
                lines=[f"</ {self.widget_spec.widget_class_name}>"],
            )


def _get_component_import_path(widget_spec, parent_module_name):
    from titan.react_view_pkg.widgetregistry import get_widget_reg

    ws_with_component_def = get_widget_reg().get(widget_spec.widget_name)
    is_same_module = parent_module_name and (
        ws_with_component_def.module_name == parent_module_name
    )
    component_name = get_component_name(ws_with_component_def)
    suffix = f"/{component_name}" if is_same_module else ""
    return (
        f"import {{ {component_name} }} from "
        + f"'src/{ws_with_component_def.module_name}/components{suffix}';"
    )
