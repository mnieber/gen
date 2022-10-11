from .add_missing_entity_fields import add_missing_entity_fields
from .strip_symbols import strip_symbols


def prepare_type_spec_dict(type_spec_dict):
    type_spec_dict = strip_symbols(type_spec_dict)
    add_missing_entity_fields(type_spec_dict)
    return type_spec_dict
