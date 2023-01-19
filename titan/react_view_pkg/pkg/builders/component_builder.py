from moonleap import append_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.widgetspec.create_widget_class_name import get_component_name


class ComponentBuilder(Builder):
    def update_widget_spec(self):
        if on_click := self.widget_spec.values.get("onClick"):
            self.widget_spec.div.append_attrs([f"onClick={{{on_click}}}"])
            append_uniq(self.widget_spec.handler_terms, "click:handler")

    def build(self):
        parent_module_name = (
            self.widget_spec.parent.module_name if self.widget_spec.parent else None
        )
        self.output.add(
            imports=[_get_component_import_path(self.widget_spec, parent_module_name)]
        )

        attrs_str = _get_attrs_str(self.widget_spec)
        class_name_attr = self.widget_spec.div.get_class_name_attr()
        key_attr = _get_key_attr(self.widget_spec)
        has_child_widgets = bool(self.widget_spec.child_widget_specs)
        if has_child_widgets:
            self.output.add(
                lines=[
                    f"<{self.widget_spec.widget_class_name} "
                    + f"{key_attr} {class_name_attr} {attrs_str}>"
                ],
            )
            self._add_child_widgets()
            self.output.add(
                lines=[f"</ {self.widget_spec.widget_class_name}>"],
            )
        else:
            self.output.add(
                lines=[
                    f"<{self.widget_spec.widget_class_name} "
                    + f"{key_attr} {class_name_attr} {attrs_str}/>"
                ],
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


def _get_attrs_str(widget_spec):
    attrs = list(widget_spec.div.attrs)

    for named_prop in widget_spec.named_props:
        required_prop_name = named_prop.name or named_prop.typ.ts_var
        data_path = _get_prop_data_path(widget_spec, named_prop)
        attrs += [f"{required_prop_name}={{{data_path}}}"]

    attrs_str = " ".join(attrs)
    return attrs_str


def _get_key_attr(widget_spec):
    key = widget_spec.div.key
    return f"key={{{key}}}" if key else ""


def _get_prop_data_path(widget_spec, named_prop):
    # The required prop must be supplied by some parent component.
    # Note that we really need "widget_spec.parent" here and not
    # "widget_spec", because the widget_spec can resolve the data path from
    # the widget props, but the component builder should not do that.

    data_path = widget_spec.parent.get_data_path(obj=named_prop, recurse=True)
    if not data_path:
        raise Exception(
            f"Could not find data path for {named_prop} "
            + f"in {widget_spec.widget_class_name}"
        )
    return data_path
