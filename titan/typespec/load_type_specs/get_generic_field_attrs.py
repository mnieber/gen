def get_generic_field_attrs(key, value_parts):
    field_attrs = dict(field_type=None, default_value=None, choices=None)

    if f"optional" in value_parts:
        field_attrs["is_optional"] = True

    if f"omit_model" not in value_parts:
        field_attrs["has_model"] = True

    if f"omit_api" not in value_parts:
        field_attrs["has_api"] = True

    if "is_inverse" in value_parts:
        field_attrs["is_inverse"] = True

    field_attrs["key"] = key.strip()

    return field_attrs
