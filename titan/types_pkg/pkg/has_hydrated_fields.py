def has_hydrated_fields(type_spec, skip=None):
    if skip is None:
        skip = []
    skip.append(type_spec.type_name)

    for field_spec in type_spec.get_field_specs():
        if is_hydrated_field(field_spec):
            return True

    for field_spec in type_spec.get_field_specs(["fk", "relatedSet"]):
        if field_spec.has_model:
            target_type_spec = field_spec.target_type_spec
            if target_type_spec.type_name not in skip:
                if has_hydrated_fields(target_type_spec, skip):
                    return True
    return False


def is_hydrated_field(field_spec):
    return field_spec.has_model and not field_spec.has_api
