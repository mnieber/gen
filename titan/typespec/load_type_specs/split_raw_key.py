from moonleap import append_uniq
from moonleap.utils.pop import pop
from moonleap.utils.split_symbols import split_symbols


def split_raw_key(key):
    key, parts = strip_generic_symbols(key)
    key, symbols = split_symbols(key)

    return key.strip(), symbols, parts


def strip_generic_symbols(key):
    parts = list()

    key, omit_model = pop(key, "^")
    if omit_model:
        append_uniq(parts, f"omit_model")

    key, omit_api = pop(key, "|")
    if omit_api:
        parts.append(f"omit_api")

    key, optional = pop(key, "?")
    if optional:
        append_uniq(parts, f"optional")

    key, is_help = pop(key, "/")
    if is_help:
        parts.append("help")

    key, admin_inline = pop(key, "=")
    if admin_inline:
        parts.append("admin_inline")

    return key, parts
