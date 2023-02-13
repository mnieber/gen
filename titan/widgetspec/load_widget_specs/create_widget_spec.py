from titan.widgetspec.widget_spec import WidgetSpec

from .get_widget_attrs import get_widget_attrs


def create_widget_spec(key, value, module_name):
    is_dict = isinstance(value, dict)
    spec = value if is_dict else {}
    widget_values = get_widget_attrs(key)

    widget_spec = WidgetSpec(**widget_values)
    widget_spec.module_name = module_name
    widget_spec.src_dict = spec

    return widget_spec, spec
