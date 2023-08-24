from moonleap import append_uniq


def add_field_spec(type_spec, field_spec):
    type_spec.add_field_spec(field_spec)

    if field_spec.display:
        type_spec.display_field = field_spec

    if field_spec.admin_search:
        append_uniq(type_spec.admin_search_by, field_spec.key)
