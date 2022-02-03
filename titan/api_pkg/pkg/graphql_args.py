import os


def _field_spec_to_graphql_type(field_spec):
    postfix = "!" if field_spec.required else ""

    if field_spec.field_type in ("string", "json", "url", "slug"):
        return "String" + postfix

    if field_spec.field_type in ("boolean",):
        return "Boolean" + postfix

    if field_spec.field_type in ("int",):
        return "Int" + postfix

    if field_spec.field_type in ("float",):
        return "Float" + postfix

    if field_spec.field_type in ("uuid",):
        return "ID" + postfix

    if field_spec.field_type in ("form",):
        return f"{field_spec.target_type_spec.type_name}Type" + postfix

    if field_spec.field_type in ("idList",):
        return r"[String]" + postfix

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
