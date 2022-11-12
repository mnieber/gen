from titan.widgets_pkg.pkg.widget_spec import WidgetSpec


def update_or_create_widget_spec(
    widget_reg, widget_type, module_name, parent_widget_spec
):
    widget_spec = widget_reg.get(widget_type, default=None)
    if not widget_spec:
        widget_spec = WidgetSpec(widget_type=widget_type, attr_specs=[])
        widget_reg.setdefault(widget_type, widget_spec)

    # Update module name
    if module_name:
        if widget_spec.module_name and widget_spec.module_name != module_name:
            raise Exception(
                f"Widget {widget_spec.widget_type} is defined in two modules: "
                + f"{widget_spec.module_name} and {module_name}"
            )
        widget_spec.module_name = module_name

    # Register parent
    if parent_widget_spec:
        widget_reg.register_parent_child(
            parent_widget_spec.widget_type, widget_spec.widget_type
        )

    return widget_spec
