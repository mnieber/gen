def maybe_make_fks_optional(type_spec_store, type_spec):
    optional_fk_field_specs = []
    for field_spec in type_spec.get_field_specs(["fk"]):
        if field_spec.is_reverse_of_related_set:
            target_type_spec = type_spec_store.get(field_spec.target)
            related_field_spec = target_type_spec.get_field_spec(
                field_spec.is_reverse_of_related_set.name, False
            )
            if related_field_spec and related_field_spec.field_type == "relatedSet":
                assert (
                    related_field_spec.through or related_field_spec.target
                ) == type_spec.type_name
                optional_fk_field_specs.append(field_spec)
    if len(optional_fk_field_specs) > 1:
        for field_spec in optional_fk_field_specs:
            field_spec.required = False
