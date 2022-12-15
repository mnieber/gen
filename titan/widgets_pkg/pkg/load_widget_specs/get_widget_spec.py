from moonleap.utils.split_non_empty import split_non_empty
from titan.widgets_pkg.pkg.widget_spec import Div, WidgetSpec

from .get_widget_attrs import get_widget_attrs


def get_widget_spec(key, value, module_name):
    is_dict = isinstance(value, dict)
    value_parts = split_non_empty(
        _get_type_value(value) if is_dict else "" if value == "pass" else value, "."
    )
    spec = value if is_dict else {}
    widget_values, div_attrs = get_widget_attrs(key, value_parts)
    widget_spec = WidgetSpec(**widget_values)
    widget_spec.div = Div(**div_attrs)
    widget_spec.module_name = module_name
    widget_spec.src_dict = spec
    return widget_spec, spec


# Find all keys in spec of type "__attrs__~ " (with k tildes and k spaces)
# and return the concatenated values of these keys
def _get_type_value(spec):
    parts = []
    for key, value in spec.items():
        clean_key = key.strip()
        while clean_key.endswith("~"):
            clean_key = clean_key[:-1].strip()

        if clean_key == "__attrs__":
            if not isinstance(value, str):
                raise Exception(f"__attrs__ must be a string: {value}")
            parts.append(value)

    return ".".join(parts)
