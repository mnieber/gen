def recurse_type_specs(type_spec, result=None):
    result = [] if result is None else result
    if type_spec in result:
        return result

    result.append(type_spec)
    for field_spec in type_spec.get_field_specs(["fk", "relatedSet", "form"]):
        recurse_type_specs(field_spec.target_type_spec, result)
    return result
