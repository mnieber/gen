from moonleap.utils.split_non_empty import split_non_empty
from titan.widgets_pkg.pkg.widget_spec import WidgetSpec

from .get_widget_attrs import get_widget_attrs


def get_widget_spec(key, raw_value):
    parts = (
        split_non_empty(raw_value.get("__type__", ""), ".")
        if isinstance(raw_value, dict)
        else []
    )
    widget_values = get_widget_attrs(key, parts)

    widget_spec = WidgetSpec(**widget_values)
    return widget_spec
