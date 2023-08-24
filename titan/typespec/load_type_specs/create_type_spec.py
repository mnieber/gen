from titan.typespec.type_spec import TypeSpec


def create_type_spec(type_name, base_type_name, parts, module_name):
    type_spec = TypeSpec(type_name=type_name, field_specs=[], module_name=module_name)
    if base_type_name:
        type_spec.base_type_name = base_type_name

    if "is_sorted" in parts:
        type_spec.is_sorted = True

    if "entity" in parts:
        type_spec.is_entity = True

    if "extract_gql_fields" in parts:
        type_spec.extract_gql_fields = True

    return type_spec
