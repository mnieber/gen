from moonleap.utils.pop import pop

from .split_raw_key import split_raw_key


def strip_fk_symbols(key):
    key, symbols, parts = split_raw_key(key)
    words = symbols.split(",")

    symbols, is_sorted = pop(symbols, ">")
    if is_sorted or "sorted" in words:
        parts.append("is_sorted")

    symbols, is_inverse = pop(symbols, "<")
    if is_inverse or "inverse" in words:
        parts.append("is_inverse")

    symbols, extract_gql_fields = pop(symbols, "&")
    if extract_gql_fields or "extract_gql_fields" in words:
        parts.append("extract_gql_fields")

    symbols, is_entity = pop(symbols, "@")
    if is_entity or "entity" in words:
        parts.append("entity")

    symbols, no_api = pop(symbols, "|")
    if no_api or "no_api" in words:
        parts.append("no_api")

    return key, parts
