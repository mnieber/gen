import typing as T

from moonleap import append_uniq
from moonleap.utils.split_non_empty import split_non_empty
from moonleap.utils.split_symbols import split_symbols
from titan.widgetspec.styles import is_style


def get_widget_attrs(key):
    attrs = dict(widget_name=None, place=None, widget_base_types=[], styles=[])

    parts_with = key.split(" with ")
    if len(parts_with) == 2:
        attrs["place"] = parts_with[0]
        key = parts_with[1]

    if key == "children":
        widget_base_types_str = "Children"
        widget_name = "Children"
    else:
        parts_as = key.split(" as ")
        widget_name = parts_as[0] if len(parts_as) == 2 else None
        widget_base_types_str = parts_as[-1]
        # The ":" is a separator used in widget names. If this separator appears
        # in the widget_base_types_str, then it means that this is really the
        # widget_name and the widget_base_types_str is empty.
        if ":" in widget_base_types_str and not widget_name:
            widget_name, styles_str = split_symbols(widget_base_types_str)
            widget_base_types_str = f"[{styles_str}]"

    if widget_name:
        attrs["widget_name"] = widget_name

    # Determine styles and widget_base_types
    for widget_base_type_str in split_non_empty(widget_base_types_str):
        widget_base_type_str, symbols = split_symbols(widget_base_type_str)
        if widget_base_type_str:
            append_uniq(attrs["widget_base_types"], widget_base_type_str)
        for style in split_non_empty(symbols):
            assert is_style(style)
            append_uniq(attrs["styles"], style)

    return attrs
