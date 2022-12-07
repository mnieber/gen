import re

from moonleap.utils.fp import append_uniq
from moonleap.utils.quote import quote
from moonleap.utils.split_non_empty import split_non_empty
from titan.types_pkg.pkg.load_type_specs.split_raw_key import split_symbols


def get_widget_attrs(key, value_parts):
    attrs = dict(div_styles=[], values={}, widget_base_types=[])
    symbol_parts = []

    parts_with = key.split(" with ")
    if len(parts_with) == 2:
        attrs["place"] = parts_with[0]
        key = parts_with[1]

    if key == "children":
        widget_base_types_str = "Children"
        widget_name = "Children"
    else:
        parts_as = key.split(" as ")

        widget_base_types_str = parts_as[-1]
        widget_base_types_str, symbols = split_symbols(widget_base_types_str)
        symbol_parts.extend(split_non_empty(symbols, "."))

        widget_name = parts_as[0] if len(parts_as) == 2 else None
        if widget_name:
            widget_name, symbols = split_symbols(widget_name)
            symbol_parts.extend(split_non_empty(symbols, "."))

        if ":" in widget_base_types_str and not widget_name:
            widget_name, widget_base_types_str = widget_base_types_str, widget_name

        for label in ("array", "capture"):
            prefix = f"{label} of"
            if widget_name and widget_name.startswith(prefix):
                widget_name = widget_name[len(prefix) :].strip()
                symbol_parts.append(f"{label}=true")

    if widget_name:
        attrs["widget_name"] = widget_name

    if widget_base_types_str:
        attrs["widget_base_types"] = widget_base_types_str.split(", ")

    for part in symbol_parts + value_parts:
        if _is_style(part):
            append_uniq(attrs["div_styles"], quote(part))
        else:
            parts_eq = part.split("=")
            if len(parts_eq) == 2:
                attrs["values"][parts_eq[0]] = parts_eq[1]
            else:
                raise Exception(f"Invalid part: {part}")

    return attrs


style_patterns = [
    r"text-(.+)-([0-9]+)",
    r"bg-(.+)-([0-9]+)",
    r"p-([0-9]+)",
    r"px-([0-9]+)",
    r"py-([0-9]+)",
    r"m-([0-9]+)",
    r"mx-([0-9]+)",
    r"my-([0-9]+)",
    r"rounded",
    r"rounded-(.+)",
]


def _is_style(part):
    for style_pattern in style_patterns:
        if re.fullmatch(style_pattern, part):
            return True
    return False
