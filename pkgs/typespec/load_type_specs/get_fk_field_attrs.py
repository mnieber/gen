from .foreign_key import ForeignKey
from .get_generic_field_attrs import get_generic_field_attrs


def get_fk_field_attrs(host, fk: ForeignKey):
    field = get_generic_field_attrs(host, fk.var, fk.parts)
    _get_field_attrs(fk.parts, fk.var_type, fk.field_type, field)

    return field


def _get_field_attrs(field_parts, var_type, field_type, field_attrs):
    if "set_null" in field_parts:
        field_attrs["set_null"] = True

    if "admin_inline" in field_parts:
        field_attrs["admin_inline"] = True

    if "help" in field_parts:
        field_attrs["help"] = True

    field_attrs["target"] = var_type
    field_attrs["field_type"] = field_type
