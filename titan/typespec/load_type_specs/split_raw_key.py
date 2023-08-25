from moonleap.utils.split_symbols import split_symbols
from titan.typespec.load_type_specs.strip_generic_symbols import strip_generic_symbols


def split_raw_key(key):
    key, parts = strip_generic_symbols(key)
    key, symbols = split_symbols(key)

    return key.strip(), symbols, parts
