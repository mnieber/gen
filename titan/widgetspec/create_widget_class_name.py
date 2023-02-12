import ramda as R

from moonleap import kebab_to_camel, u0


def create_widget_class_name(widget_spec):
    if widget_spec.is_component:
        return get_component_name(widget_spec)
    else:
        assert widget_spec.parent

    default_class_name = u0(
        widget_spec.widget_name
        or widget_spec.place
        or R.last(widget_spec.widget_base_types)
    )
    widget_class_name = widget_spec.values.get("class", default_class_name)

    shorten = widget_class_name.startswith("__")
    if shorten:
        root = widget_spec.root
        # The name "__" is a shorthand for __ + default_class_name
        suffix = default_class_name if widget_class_name == "__" else ""
        prefix = "" if root is widget_spec else root.widget_class_name
        return prefix + widget_class_name + suffix
    else:
        root = widget_spec.parent
        infix = "__" if root.is_component else ""
        return root.widget_class_name + infix + widget_class_name


def get_component_name(widget_spec):
    name, tag = widget_spec.widget_name.split(":")
    if name.endswith("-"):
        name += tag
    widget_kebab_name = name.replace("-:", "-").replace(":", "-")
    result = u0(kebab_to_camel(widget_kebab_name))
    return result
