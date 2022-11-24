from moonleap import u0
from moonleap.utils.inflect import singular


def create_widget_class_name(widget_spec, parent_builder):
    widget_class_name = (
        _to_widget_class_name(widget_spec)
        or widget_spec.place
        or widget_spec.widget_base_type
    )
    if widget_spec.is_component:
        return widget_class_name

    if parent_builder and widget_class_name:
        parent_widget_spec = parent_builder.widget_spec
        infix = "__" if parent_widget_spec.is_component else ""
        return parent_builder.output.widget_class_name + infix + widget_class_name

    return widget_class_name


def _to_widget_class_name(widget_spec):
    if not widget_spec.is_component:
        default_class_name = widget_spec.widget_name
        if widget_spec.values.get("array", False):
            default_class_name = singular(default_class_name)
        class_name = widget_spec.values.get("cn", default_class_name)
        return u0(class_name)
    return widget_spec.component.name
