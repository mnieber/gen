from moonleap.utils.merge_into_config import merge_into_config
from moonleap.utils.split_non_empty import split_non_empty
from titan.widgetspec.div import Div
from titan.widgetspec.widget_spec import WidgetSpec

from .get_widget_attrs import get_widget_attrs


def create_widget_spec(key, value, module_name):
    is_dict = isinstance(value, dict)
    spec = value if is_dict else {}
    widget_values, styles = get_widget_attrs(key)

    widget_spec = WidgetSpec(**widget_values, values=_get_attrs(spec, "__dict__"))
    widget_spec.div = Div(
        styles=styles, attrs=_to_div_attrs(_get_attrs(spec, "__set__"))
    )
    widget_spec.module_name = module_name
    widget_spec.src_dict = spec

    return widget_spec, spec


# Find all keys in spec of type "__set__~ " (with k tildes and k spaces)
# and return the merged values of these keys
def _get_attrs(spec, attrs_key):
    result = {}
    for key, value in spec.items():
        clean_key = key.strip()
        while clean_key.endswith("~"):
            clean_key = clean_key[:-1].strip()

        if clean_key == attrs_key:
            if not isinstance(value, dict):
                raise Exception(f"{attrs_key} must be a dict: {value}")
            merge_into_config(result, value)

    return result


def _to_div_attrs(attrs):
    return [f"{key}={value}" for key, value in attrs.items()]
