from moonleap.utils.pop import pop

from .strip_generic_symbols import strip_generic_symbols


def strip_fk_symbols(key):
    key, parts = strip_generic_symbols(key)

    key, is_parent = pop(key, "$")
    if is_parent:
        parts.append("is_parent")

    key, is_sorted = pop(key, ">")
    if is_sorted:
        parts.append("is_sorted")

    key, is_sorted = pop(key, "&")
    if is_sorted:
        parts.append("extract_gql_fields")

    key, is_sorted = pop(key, "!")
    if is_sorted:
        parts.append("help")

    key, admin_inline = pop(key, "=")
    if admin_inline:
        parts.append("admin_inline")

    key, is_entity = pop(key, "@")
    if is_entity:
        parts.append("entity")

    return key, parts
