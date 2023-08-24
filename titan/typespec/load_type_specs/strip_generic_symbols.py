from moonleap import append_uniq
from moonleap.utils.pop import pop


def strip_generic_symbols(key):
    parts = list()

    key, omit_model = pop(key, "^")
    if omit_model:
        append_uniq(parts, f"omit_model")

    key, no_api = pop(key, "|")
    if no_api:
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
