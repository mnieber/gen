from .get_generic_field_attrs import get_generic_field_attrs


def get_fk_field_attrs(host, key, data, init_parts):
    field = get_generic_field_attrs(host, key, init_parts)
    _get_field_attrs(init_parts, data, field)

    return field


def _get_field_attrs(field_parts, data, field_attrs):
    if "set_null" in field_parts:
        field_attrs["set_null"] = True

    if "admin_inline" in field_parts:
        field_attrs["admin_inline"] = True

    if "help" in field_parts:
        field_attrs["help"] = True

    field_attrs["target"] = data.var_type
    field_attrs["field_type"] = data.field_type
