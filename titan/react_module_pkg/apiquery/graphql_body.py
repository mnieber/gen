import os


def graphql_body(type_spec, indent=0, skip=None, recurse=True):
    is_top_level = not skip
    skip = skip or [type_spec.type_name]

    result = []
    for field_spec in type_spec.field_specs:
        if field_spec.field_type in ("fk", "relatedSet"):
            if field_spec.field_type == "fk" and not is_top_level:
                result.append(f"{field_spec.name}Id")
            target_type_spec = field_spec.target_type_spec
            if (is_top_level or recurse) and target_type_spec.type_name not in skip:
                include_field_name = field_spec.field_type in ("fk", "relatedSet")
                if include_field_name:
                    result.append(f"{field_spec.name} {{")
                    indent += 2
                result.extend(
                    graphql_body(
                        target_type_spec,
                        indent,
                        skip + [target_type_spec.type_name],
                        recurse=recurse,
                    )
                )
                if include_field_name:
                    indent -= 2
                    result.append(f"}}")
        else:
            result.append(f"{field_spec.name}")

    if is_top_level:
        return " " * 10 + (os.linesep + (" " * 10)).join(result)
    else:
        return [(" " * indent) + x for x in result]
