def has_derived_fields(type_spec, host, skip=None):
    if type_spec.type_name == "ParameterType":
        __import__("pudb").set_trace()
    if skip is None:
        skip = []
    skip.append(type_spec.type_name)

    for field_spec in type_spec.get_field_specs():
        if host in field_spec.has_model and host not in field_spec.has_api:
            return True

    for field_spec in type_spec.get_field_specs(["fk", "relatedSet"]):
        if host in field_spec.has_model:
            target_type_spec = field_spec.target_type_spec
            if target_type_spec.type_name not in skip:
                if has_derived_fields(target_type_spec, host, skip):
                    return True
    return False
