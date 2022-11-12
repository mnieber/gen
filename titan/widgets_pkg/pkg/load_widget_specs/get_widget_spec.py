from titan.widgets_pkg.pkg.widget_spec import WidgetSpec

from .get_widget_attrs import get_widget_attrs


def get_widget_spec(key, raw_value):
    widget_values = get_widget_attrs(key)

    widget_spec = WidgetSpec(**widget_values)
    return widget_spec
