from moonleap import append_uniq


def add_field_spec(type_spec, field_spec):
    # Check if matching auto fields have previously been added for this field_spec
    auto_field_specs = _get_matching_field_specs(type_spec, field_spec, is_auto=True)

    if field_spec.is_auto:
        # Check if the new auto field_spec matches with an existing auto field.
        # This is only okay if it matches exactly.
        for auto_field_spec in auto_field_specs:
            if auto_field_spec == field_spec:
                return False

        # Check if a normal field spec already exists for this key. In that case,
        # ignore this auto field spec.
        if type_spec.get_field_spec_by_key(field_spec.key):
            return False

        if auto_field_specs:
            raise Exception(
                "A similar auto field spec already exists."
                + f"Existing field specs: {auto_field_specs}. "
                + f"New field spec: {field_spec}"
            )
    else:
        # We're adding a normal field spec. Remove matching auto field
        # specs (they are replaced by the new field spec).
        for auto_field_spec in auto_field_specs:
            _remove_field_spec_by_key(type_spec, auto_field_spec.key)

    type_spec.add_field_spec(field_spec)

    if field_spec.display:
        type_spec.display_field = field_spec

    if field_spec.admin_search:
        append_uniq(type_spec.admin_search_by, field_spec.key)

    if field_spec.select:
        append_uniq(type_spec.select_by, field_spec.key)

    return True


def _get_matching_field_specs(type_spec, field_spec, is_auto):
    result = []
    candidate_field_specs = [
        x for x in type_spec.field_specs if bool(x.is_auto) == is_auto
    ]
    for candidate_field_spec in candidate_field_specs:
        if candidate_field_spec.key == field_spec.key:
            result.append(candidate_field_spec)
        else:
            if (
                field_spec.field_type == "fk"
                and candidate_field_spec.field_type == "fk"
            ):
                if candidate_field_spec.target == field_spec.target:
                    result.append(candidate_field_spec)
    return result


def _remove_field_spec_by_key(type_spec, key):
    field_spec = type_spec.get_field_spec_by_key(key)
    assert field_spec
    type_spec.remove_field_spec_by_key(key)

    if type_spec.admin_search_by:
        type_spec.admin_search_by = [x for x in type_spec.admin_search_by if x != key]

    if type_spec.select_by:
        type_spec.select_by = [x for x in type_spec.select_by if x != key]

    if type_spec.display_field and type_spec.display_field.key == key:
        type_spec.display_field = None
