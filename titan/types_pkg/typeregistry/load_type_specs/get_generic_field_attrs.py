def get_generic_field_attrs(host, key, value_parts):
    field_attrs = dict(field_type=None, default_value=None, choices=None)

    if "auto" in value_parts:
        field_attrs["is_auto"] = True

    if "related_fk" in value_parts:
        field_attrs["is_related_fk"] = True

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

    field_attrs["key"] = key.strip()

    return field_attrs
