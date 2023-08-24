def add_type_spec_to_type_reg(type_reg, type_spec, module_name, parent_type_spec):
    existing_type_spec = type_reg.get(type_spec.type_name, default=None)
    if existing_type_spec:
        for field_spec in type_spec.field_specs:
            existing_type_spec.add_field_spec(field_spec)
        if (
            module_name
            and existing_type_spec.module_name
            and existing_type_spec.module_name != module_name
        ):
            raise Exception(
                f"Type {existing_type_spec.type_name} is defined in two modules: "
                + f"{existing_type_spec.module_name} and {module_name}"
            )
        type_spec = existing_type_spec
    else:
        type_reg.setdefault(type_spec.type_name, type_spec)

    # Register parent
    if parent_type_spec:
        type_reg.register_parent_child(parent_type_spec.type_name, type_spec.type_name)

    # Update module name
    if module_name:
        type_spec.module_name = module_name
