from moonleap import append_uniq
from moonleap.utils.pop import pop


def strip_generic_symbols(key):
    parts = list()

    key, optional = pop(key, "?")
    if optional:
        append_uniq(parts, f"optional")

    key, is_indexed = pop(key, "%")
    if is_indexed:
        append_uniq(parts, f"is_indexed")

    key, is_help = pop(key, "/")
    if is_help:
        parts.append("help")

    key, admin_inline = pop(key, "=")
    if admin_inline:
        parts.append("admin_inline")

    return key, parts
