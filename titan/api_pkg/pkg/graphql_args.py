import os


def _field_spec_to_graphql_type(field_spec):
    if field_spec.field_type in ("string", "json", "url", "slug"):
        return "String"

    if field_spec.field_type in ("boolean",):
        return "Boolean"

    if field_spec.field_type in ("uuid",):
        return "ID"

    if field_spec.field_type in ("form",):
        return f"{field_spec.target_type_spec.type_name}Type"

    raise Exception(f"Cannot deduce graphql type for {field_spec.field_type}")


def declare_graphql_variable(field_spec):
    graphql_type = _field_spec_to_graphql_type(field_spec)
    return f"${field_spec.name}: {graphql_type}"


def invoke_graphql_variable(field_spec):
    return f"{field_spec.short_name}: ${field_spec.name}"


def graphql_args(field_specs, before, base_indent=4):
    if not field_specs:
        return ""

    tab = " " * (base_indent if before else base_indent + 4)
    result = ["("]
    for field_spec in field_specs:
        if before:
            result.append(f"{tab}  {declare_graphql_variable(field_spec)}")
        else:
            result.append(f"{tab}  {invoke_graphql_variable(field_spec)}")
    result += [f"{tab})"]
    return os.linesep.join(result)
