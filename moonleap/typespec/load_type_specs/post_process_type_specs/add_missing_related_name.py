def add_missing_related_name(type_spec):
    for fk_field_spec in type_spec.get_field_specs(["fk"]):
        if fk_field_spec.is_reverse_of_related_set:
            fk_field_spec.related_name = fk_field_spec.is_reverse_of_related_set.name
