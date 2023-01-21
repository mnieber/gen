from moonleap import append_uniq
from moonleap.utils.quote import quote
from moonleap.utils.split_non_empty import split_non_empty
from moonleap.utils.split_symbols import split_symbols
from titan.widgetspec.is_style import is_style


def get_widget_attrs(key, more_value_parts):
    div_attrs = dict(styles=[], attrs=[])
    attrs = dict(values={}, place_values={}, widget_base_types=[])

    parts_with = key.split(" with ")
    if len(parts_with) == 2:
        place = parts_with[0]
        place, place_symbols = split_symbols(place)
        attrs["place"] = place
        place_symbol_parts = split_non_empty(place_symbols)
        key = parts_with[1]
    else:
        place_symbol_parts = []

    if key == "children":
        widget_base_types_str = "Children"
        widget_name = "Children"
        symbol_parts = []
    else:
        parts_as = key.split(" as ")
        widget_name = parts_as[0] if len(parts_as) == 2 else None
        widget_base_types_str = parts_as[-1]
        # The ":" is a separator used in widget names. If this separator appears
        # in the widget_base_types_str, then it means that this is really the
        # widget_name and the widget_base_types_str is empty.
        if ":" in widget_base_types_str and not widget_name:
            widget_name, widget_base_types_str = widget_base_types_str, ""

        symbol_parts = []
        for label in ("array", "capture"):
            prefix = f"{label} of"
            if widget_name and widget_name.startswith(prefix):
                widget_name = widget_name[len(prefix) :].strip()
                symbol_parts.append(f"{label}=true")

    attrs["widget_base_types"] = list()
    for widget_base_type_str in split_non_empty(widget_base_types_str):
        widget_base_type_str, symbols = split_symbols(widget_base_type_str)
        append_uniq(attrs["widget_base_types"], widget_base_type_str)
        for symbol_part in split_non_empty(symbols):
            symbol_parts.append(symbol_part)

    if widget_name:
        attrs["widget_name"] = widget_name

    for part in symbol_parts + more_value_parts:
        if is_style(part):
            append_uniq(div_attrs["styles"], quote(part))
        else:
            parts_eq = part.split("=")
            if len(parts_eq) == 2:
                key = parts_eq[0]
                if key in attrs["values"]:
                    raise Exception(f"Duplicate key: {key}")
                attrs["values"][key] = parts_eq[1]
            else:
                raise Exception(f"Invalid part: {part}")

    for part in place_symbol_parts:
        if is_style(part):
            pass
        else:
            parts_eq = part.split("=")
            if len(parts_eq) == 2:
                attrs["place_values"][parts_eq[0]] = parts_eq[1]
            else:
                raise Exception(f"Invalid part: {part}")

    return attrs, div_attrs
