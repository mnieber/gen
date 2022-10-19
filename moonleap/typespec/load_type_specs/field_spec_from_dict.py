from .foreign_key import ForeignKey
from .get_fk_field_spec import get_fk_field_spec
from .get_scalar_field_spec import get_scalar_field_spec
from .strip_generic_symbols import strip_generic_symbols


def field_spec_from_dict(host, key, value):
    flag_is_related_fk = is_related_fk(value)
    flag_is_pass = is_pass(value)
    if flag_is_related_fk or flag_is_pass:
        value = {"__init__": ".".join(value.split(".")[1:])}
    is_fk = isinstance(value, dict)

    if is_fk:
        fk = ForeignKey(key, value)
        field_spec = get_fk_field_spec(host, fk)
        return dict(
            is_fk=is_fk,
            fk=fk,
            new_value=value,
            field_spec=field_spec,
            is_related_fk=flag_is_related_fk,
            is_pass=flag_is_pass,
        )
    else:
        new_key, value_parts = strip_generic_symbols(key)
        new_value = ".".join(value.split(".") + value_parts)
        field_spec = get_scalar_field_spec(host, new_key, new_value)
        return dict(
            is_fk=is_fk, new_key=new_key, new_value=new_value, field_spec=field_spec
        )


def is_related_fk(value):
    return isinstance(value, str) and value.split(".")[0] == "RelatedFk"


def is_pass(value):
    return value == "pass"
