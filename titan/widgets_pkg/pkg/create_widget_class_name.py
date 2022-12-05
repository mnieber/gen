from moonleap import u0


def create_widget_class_name(builder):
    widget_class_name = (
        _to_widget_class_name(builder.widget_spec)
        or builder.widget_spec.place
        or builder.widget_spec.widget_base_type
    )
    if builder.widget_spec.is_component:
        return widget_class_name

    if widget_class_name:
        shorten = widget_class_name.startswith("__")
        root = builder.root_builder if shorten else builder.parent_builder
        if root and root is not builder:
            infix = "__" if root.widget_spec.is_component and not shorten else ""
            return root.output.widget_class_name + infix + widget_class_name

    return widget_class_name


def _to_widget_class_name(widget_spec):
    if not widget_spec.is_component:
        default_class_name = (
            widget_spec.widget_name or widget_spec.place or widget_spec.widget_base_type
        )
        class_name = widget_spec.values.get("cn", default_class_name)

        # The name "__" is a shorthand
        if class_name == "__":
            class_name += default_class_name

        return u0(class_name)
    return widget_spec.component.name