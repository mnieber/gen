def get_generic_field_attrs(key, value_parts):
    field_attrs = dict(field_type=None, default_value=None, choices=None)

    field_attrs["derived"] = "derived" in value_parts
    field_attrs["required"] = "optional" not in value_parts
    field_attrs["api"] = []
    if "server_api" in value_parts or "no_api" not in value_parts:
        field_attrs["api"].append("server")
    if "client_api" in value_parts or "no_api" not in value_parts:
        field_attrs["api"].append("client")
    field_attrs["key"] = key.strip()

    return field_attrs
