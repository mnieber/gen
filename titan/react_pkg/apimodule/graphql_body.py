import os

from moonleap.utils.case import l0


def graphql_body(
    type_spec, indent=0, skip=None, recurse=True, type_specs_to_import=None
):
    is_top_level = not skip
    skip = skip or [type_spec.type_name]
    if type_specs_to_import is None:
        type_specs_to_import = []

    result = []
    if type_spec.extract_gql_fields:
        type_specs_to_import.append(type_spec)
        result.append(" " * indent + "${" + l0(type_spec.type_name) + "GqlFields}")
    else:
        field_specs = [
            x
            for x in sorted(list(type_spec.get_field_specs()), key=lambda x: x.name)
            if "client" in x.api
        ]

        for field_spec in field_specs:
            if field_spec.field_type not in ("fk", "relatedSet"):
                result.append(" " * indent + f"{field_spec.name}")

        for field_spec in field_specs:
            if field_spec.field_type in ("fk", "relatedSet"):
                target_type_spec = field_spec.target_type_spec
                if (is_top_level or recurse) and target_type_spec.type_name not in skip:
                    include_field_name = field_spec.field_type in ("fk", "relatedSet")
                    if include_field_name:
                        result.append(" " * indent + f"{field_spec.name} {{")
                        indent += 2
                    result.extend(
                        graphql_body(
                            target_type_spec,
                            indent,
                            skip + [target_type_spec.type_name],
                            recurse=recurse,
                            type_specs_to_import=type_specs_to_import,
                        )
                    )
                    if include_field_name:
                        indent -= 2
                        result.append(" " * indent + "}")

    if is_top_level:
        return type_specs_to_import, (os.linesep + (" " * 10)).join(result)
    else:
        return result


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
