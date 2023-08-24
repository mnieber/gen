def get_generic_field_attrs(host, key, value_parts):
    field_attrs = dict(field_type=None, default_value=None, choices=None)

    field_attrs["optional"] = []
    if f"optional" in value_parts:
        if f"required" not in value_parts:
            field_attrs["optional"].append(host)
    if f"required" in value_parts:
        field_attrs["optional"].append(f"required_{host}")

    field_attrs["has_model"] = []
    if f"omit_model" not in value_parts:
        field_attrs["has_model"].append(host)

    field_attrs["has_api"] = []
    if f"omit_api" not in value_parts:
        field_attrs["has_api"].append(host)

    if "is_inverse" in value_parts:
        field_attrs["is_inverse"] = True

    field_attrs["key"] = key.strip()

    return field_attrs
