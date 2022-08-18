def get_target_type_spec(type_spec_store, fk_field_spec):
    target_type_name = fk_field_spec.through or fk_field_spec.target
    if target_type_name == "+":
        return None
    return type_spec_store.get(target_type_name)
