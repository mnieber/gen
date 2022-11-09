import re

from titan.types_pkg.pkg.load_type_specs.split_raw_key import split_symbols


def get_widget_attrs(key):
    attrs = dict(styles=[], values=[])

    parts_as = key.split(" as ")
    widget_type = parts_as[-1]

    if len(parts_as) > 1:
        attrs["widget_name"] = widget_name = parts_as[0]

    attrs["widget_type"], symbols = split_symbols(widget_type)
    if attrs["widget_type"][0].isupper():
        raise Exception("Widget type must be lowercase: " + widget_type)

    for symbol in symbols.split("."):
        if _is_style(symbol):
            attrs["styles"].append(symbol)
        else:
            attrs["values"].append(symbol)

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


def _is_style(symbol):
    for style_pattern in style_patterns:
        if re.fullmatch(style_pattern, symbol):
            return True
    return False
