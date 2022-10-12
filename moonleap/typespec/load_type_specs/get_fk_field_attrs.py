from .get_generic_field_attrs import get_generic_field_attrs


def get_fk_field_attrs(host, key, foo, bar, init_parts, init_target_parts):
    is_speccing_through_type = bar and bar.var_type

    field_parts = init_target_parts if is_speccing_through_type else init_parts
    field = get_generic_field_attrs(host, key, field_parts)
    _get_field_attrs(field_parts, foo, field)

    if is_speccing_through_type:
        field["through"] = bar.var_type
        if bar.var:
            field["through_var"] = bar.var

    return field


def _get_field_attrs(field_parts, foo, field_attrs):
    if "set_null" in field_parts:
        field_attrs["set_null"] = True

    if "admin_inline" in field_parts:
        field_attrs["admin_inline"] = True

    if "help" in field_parts:
        field_attrs["help"] = True

    field_attrs["target"] = foo.var_type
    field_attrs["field_type"] = foo.field_type
