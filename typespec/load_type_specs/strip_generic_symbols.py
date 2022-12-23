from moonleap import append_uniq
from moonleap.utils.pop import pop


def strip_generic_symbols(key):
    parts = list()
    key, removed = pop(key, "*")

    key, no_model = pop(key, "^")
    if no_model or removed:
        append_uniq(parts, f"omit_model")

    key, no_api = pop(key, "|")
    if no_api or removed:
        parts.append(f"omit_api")

    key, optional = pop(key, "?")
    if optional:
        append_uniq(parts, f"optional")

    key, required = pop(key, "!")
    if required:
        append_uniq(parts, f"required")

    key, is_help = pop(key, "/")
    if is_help:
        parts.append("help")

    key, admin_inline = pop(key, "=")
    if admin_inline:
        parts.append("admin_inline")

    return key, parts
