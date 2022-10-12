from moonleap.utils.pop import pop

from .strip_generic_symbols import strip_generic_symbols


def strip_fk_symbols(key):
    key, parts = strip_generic_symbols(key)

    key, is_sorted = pop(key, ">")
    if is_sorted:
        parts.append("is_sorted")

    key, extract_gql_fields = pop(key, "&")
    if extract_gql_fields:
        parts.append("extract_gql_fields")

    key, is_entity = pop(key, "@")
    if is_entity:
        parts.append("entity")

    return key, parts
