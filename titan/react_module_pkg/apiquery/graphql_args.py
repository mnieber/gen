import os


def _field_spec_to_graphql_type(field_spec):
    if field_spec.field_type in ("string", "json", "url"):
        return "String"

    if field_spec.field_type in ("boolean",):
        return "Boolean"

    if field_spec.field_type in ("uuid",):
        return "ID"

    if field_spec.field_type in ("form",):
        return f"{field_spec.fk_type_spec.type_name}Type"

    raise Exception(f"Cannot deduce graphql type for {field_spec.field_type}")


def _field_spec_to_graphql_arg(field_spec, before):
    graphql_type = _field_spec_to_graphql_type(field_spec)
    if before:
        return f"${field_spec.name}: {graphql_type}"
    return f"{field_spec.name}: ${field_spec.name}"


def graphql_args(field_specs, before, base_indent=4):
    if not field_specs:
        return ""

    tab = " " * (base_indent if before else base_indent + 4)
    result = ["("]
    for field_spec in field_specs:
        result.append(f"{tab}  {_field_spec_to_graphql_arg(field_spec, before)}")
    result += [f"{tab})"]
    return os.linesep.join(result)
