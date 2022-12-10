from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.get_data_path import get_data_path


class ComponentBuilder(Builder):
    def build(self):
        self.add(imports_lines=[_get_component_import_path(self.widget_spec)])

        attrs_str = _get_attrs_str(self.widget_spec)
        key_attr = _get_key_attr(self.widget_spec)
        has_children = bool(self.widget_spec.child_widget_specs)
        if has_children:
            self.add(
                lines=[
                    f"<{self.widget_spec.widget_class_name} {key_attr} {attrs_str}>"
                ],
            )
            self._add_child_widgets()
            self.add(
                lines=[f"</ {self.widget_spec.widget_class_name}>"],
            )
        else:
            self.add(
                lines=[
                    f"<{self.widget_spec.widget_class_name} {key_attr} {attrs_str}/>"
                ],
            )


def _get_component_import_path(widget_spec):
    is_same_module = widget_spec.module_name == widget_spec.parent_ws.module_name
    suffix = f"/{widget_spec.widget_class_name}" if is_same_module else ""
    return (
        f"import {{ {widget_spec.widget_class_name} }} from "
        + f"'src/{widget_spec.module_name}/components{suffix}';"
    )


def _get_attrs_str(widget_spec):
    attrs = list(widget_spec.div_attrs)
    for named_prop in widget_spec.component.named_props:
        required_prop_name = named_prop.name or named_prop.typ.ts_var
        data_path = _get_prop_data_path(widget_spec, named_prop)
        attrs += [f"{required_prop_name}={{{data_path}}}"]
    attrs_str = " ".join(attrs)
    return attrs_str


def _get_key_attr(widget_spec):
    key = widget_spec.div_key
    return f"key={{{key}}}" if key else ""


def _get_prop_data_path(widget_spec, named_prop):
    # The required prop must be supplied by some parent component
    data_path = get_data_path(widget_spec.parent_ws, term=named_prop.meta.term)
    if not data_path:
        raise Exception(
            f"Could not find data path for {named_prop} "
            + f"in {widget_spec.widget_class_name}"
        )
    return data_path
