def set_is_reverse_of_related_set(type_spec_store, type_spec):
    # Convert string values of is_reverse_of_related_set to field specs
    for field_spec in type_spec.get_field_specs(["fk"]):
        parent_field = field_spec.is_reverse_of_related_set
        if isinstance(parent_field, str):
            parent_type_name, parent_field = parent_field.split(".")
            field_spec.is_reverse_of_related_set = type_spec_store.get(
                parent_type_name
            ).get_field_spec(parent_field)
            assert field_spec.is_reverse_of_related_set
