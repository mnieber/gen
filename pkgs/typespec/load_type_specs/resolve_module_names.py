from moonleap import append_uniq


def resolve_module_names(type_reg):
    queue = [x for x in type_reg.type_specs() if not x.module_name]
    changed = True

    while queue and changed:
        type_spec = queue.pop(0)

        module_names = []
        for parent_type_name in type_reg.parents_by_type_name.get(
            type_spec.type_name, []
        ):
            parent_type_spec = type_reg.get(parent_type_name)
            if parent_type_spec.module_name:
                append_uniq(module_names, parent_type_spec.module_name)

        if len(module_names) > 1:
            raise Exception(
                f"Cannot determine module name for {type_spec.type_name}. "
                + f"Options are: {module_names}"
            )

        if len(module_names) == 1:
            type_spec.module_name = module_names[0]
            changed = True
        else:
            queue.append(type_spec)

    if queue:
        raise Exception(
            f"Cannot determine module name for {queue[0].type_name}. "
            + "It has no parent type with a module name."
        )
