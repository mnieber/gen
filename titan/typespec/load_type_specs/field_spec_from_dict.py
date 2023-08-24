from titan.typespec.field_spec import get_field_spec_constructor

from .foreign_key import ForeignKey
from .get_fk_field_attrs import get_fk_field_attrs
from .get_scalar_field_spec import get_scalar_field_spec
from .split_raw_key import split_raw_key


def field_spec_from_dict(key, value):
    flag_is_pass = is_pass(value)
    if flag_is_pass:
        parts = value.split(",")
        value = {"__attrs__": ",".join(parts[1:])}
    is_fk = isinstance(value, dict)

    if is_fk:
        fk = ForeignKey(key, value)
        field_attrs = get_fk_field_attrs(fk)
        field_spec = get_field_spec_constructor(field_attrs["field_type"])(
            **field_attrs
        )
        return dict(
            fk=fk,
            new_value=value,
            field_spec=field_spec,
            is_pass=flag_is_pass,
        )
    else:
        new_key, symbols, value_parts = split_raw_key(key)

        new_value = ",".join(value.split(",") + value_parts)
        field_spec = get_scalar_field_spec(new_key, new_value)
        return dict(new_key=new_key, new_value=new_value, field_spec=field_spec)


def is_pass(value):
    return isinstance(value, str) and value.split(",")[0] == "pass"
