def get_generic_field_attrs(key, value_parts):
    field_attrs = dict(field_type=None, default_value=None, choices=None)

    if f"optional" in value_parts:
        field_attrs["is_optional"] = True

    if "is_inverse" in value_parts:
        field_attrs["is_inverse"] = True

    if "is_indexed" in value_parts:
        field_attrs["is_indexed"] = True

    field_attrs["key"] = key.strip()

    return field_attrs
