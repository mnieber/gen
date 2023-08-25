def process_api_spec(type_spec, api_spec, api_type_spec):
    for deleted_field in api_spec.get("__delete__", []):
        field_spec = type_spec.get_field_spec_by_key(deleted_field)
        if not field_spec:
            raise Exception(f"Field {deleted_field} not found in {type_spec.type_name}")
        field_spec.has_api = False
    for field_spec in api_type_spec.field_specs:
        field_spec.has_api = True
        field_spec.has_model = False
        type_spec.add_field_spec(field_spec)
