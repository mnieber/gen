from moonleap import kebab_to_camel, u0


def create_widget_class_name(widget_spec):
    widget_class_name = _to_widget_class_name(widget_spec)
    if widget_spec.is_component:
        return widget_class_name

    if widget_class_name:
        shorten = widget_class_name.startswith("__")
        root = widget_spec.root if shorten else widget_spec
        if root and root is not widget_spec:
            infix = "__" if root.is_component and not shorten else ""
            return root.widget_class_name + infix + widget_class_name

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

    name, tag = widget_spec.widget_name.split(":")
    if name.endswith("-"):
        name += tag
    widget_kebab_name = name.replace("-:", "-").replace(":", "-")
    return u0(kebab_to_camel(widget_kebab_name))
