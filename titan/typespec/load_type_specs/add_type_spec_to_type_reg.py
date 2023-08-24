def add_type_spec_to_type_reg(type_reg, type_spec, parent_type_spec):
    existing_type_spec = type_reg.get(type_spec.type_name, default=None)
    if existing_type_spec:
        for field_spec in type_spec.field_specs:
            existing_type_spec.add_field_spec(field_spec)
        if not existing_type_spec.module_name:
            existing_type_spec.module_name = type_spec.module_name
        type_spec = existing_type_spec
    else:
        type_reg.setdefault(type_spec.type_name, type_spec)

    # Register parent. The parent-child relationship is later used to
    # derive (when necessary) the module_name from the parent.
    if parent_type_spec:
        type_reg.register_parent_child(parent_type_spec.type_name, type_spec.type_name)
