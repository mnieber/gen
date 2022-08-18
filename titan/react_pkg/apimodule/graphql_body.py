import os

from moonleap.utils.case import l0


def graphql_body(type_spec, indent=0, skip=None, recurse=True):
    is_top_level = not skip
    skip = skip or [type_spec.type_name]

    result = []
    for field_spec in sorted(list(type_spec.get_field_specs()), key=lambda x: x.name):
        if field_spec.field_type not in ("fk", "relatedSet"):
            result.append(f"{field_spec.name}")

    for field_spec in sorted(list(type_spec.get_field_specs()), key=lambda x: x.name):
        if field_spec.field_type in ("fk", "relatedSet"):
            if field_spec.field_type == "fk" and not is_top_level:
                result.append(f"{field_spec.name}Id")
            target_type_spec = field_spec.target_type_spec
            if (is_top_level or recurse) and target_type_spec.type_name not in skip:
                include_field_name = field_spec.field_type in ("fk", "relatedSet")
                if include_field_name:
                    result.append(field_spec.name)
                    indent += 2
                if target_type_spec.extract_gql_fields:
                    result.append(
                        indent * " " + "${" + l0(target_type_spec.type_name) + "Fields}"
                    )
                else:
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
                    result.append("}")

    if is_top_level:
        return (os.linesep + (" " * 10)).join(result)
    else:
        return [(" " * indent) + x for x in result]


def get_dependency_type_specs(type_spec, skip=None, recurse=True):
    is_top_level = not skip
    skip = skip or [type_spec.type_name]

    result = []
    for field_spec in sorted(list(type_spec.get_field_specs()), key=lambda x: x.name):
        if field_spec.field_type in ("fk", "relatedSet"):
            target_type_spec = field_spec.target_type_spec
            if (is_top_level or recurse) and target_type_spec.type_name not in skip:
                if target_type_spec.extract_gql_fields:
                    if target_type_spec not in result:
                        result.append(target_type_spec)
                else:
                    result.extend(
                        get_dependency_type_specs(
                            target_type_spec,
                            skip + [target_type_spec.type_name],
                            recurse=recurse,
                        )
                    )
    return result
