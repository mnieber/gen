def set_related_name(field_spec, type_spec, keys):
    related_field_spec = None
    for key in keys:
        rhs_field_spec = type_spec.get_field_spec_by_key(key)
        if rhs_field_spec.is_inverse:
            if related_field_spec:
                raise Exception(
                    f"Multiple inverse fields in {type_spec.type_name} for {field_spec.key}"
                )
            related_field_spec = rhs_field_spec

    if not related_field_spec:
        return

    if field_spec.field_type == "relatedSet":
        if related_field_spec.field_type != "fk":
            raise Exception(
                f"Field {field_spec.key} in {type_spec.type_name} is not a fk"
            )
        related_field_spec.related_name = field_spec.name
    else:
        if related_field_spec.field_type != "relatedSet":
            raise Exception(
                f"Field {field_spec.key} in {type_spec.type_name} is not a relatedSet"
            )
        field_spec.related_name = related_field_spec.name
