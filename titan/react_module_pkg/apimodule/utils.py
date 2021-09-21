import os

import ramda as R
from moonleap import upper0
from moonleap.resources.type_spec_store import type_spec_store


def javascript_args(type_spec):
    field_specs = type_spec.field_specs
    return ", ".join(R.map(lambda t: field_spec_to_ts_arg(t.name, t), field_specs))


def field_spec_to_ts_type(field_spec):
    if field_spec.field_type in ("string", "json", "url", "slug", "uuid"):
        return "string"

    if field_spec.field_type in ("boolean",):
        return "boolean"

    if field_spec.field_type in ("fk", "related_set", "form"):
        return f"{upper0(field_spec.field_type_attrs['item_name'])}T"

    raise Exception(f"Cannot deduce typescript type for {field_spec.field_type}")


def field_spec_to_ts_arg(field_name, field_spec):
    ts_type = field_spec_to_ts_type(field_spec)
    return f"{field_name}: {ts_type}"


def _input_field_to_graphql_type(field_spec):
    if field_spec.field_type in ("string", "json", "url"):
        return "String"

    if field_spec.field_type in ("boolean",):
        return "Boolean"

    if field_spec.field_type in ("uuid",):
        return "ID"

    if field_spec.field_type in ("form",):
        return f"{field_spec.fk_type_spec.type_name}Type"

    raise Exception(f"Cannot deduce graphql type for {field_spec.field_type}")


def field_spec_to_graphql_arg(field_name, field_spec, before):
    graphql_type = _input_field_to_graphql_type(field_spec)
    if before:
        return f"${field_name}: {graphql_type}"
    return f"{field_name}: ${field_name}"


def graphql_body(type_spec, indent=0, skip=None):
    is_top_level = not skip
    if skip is None:
        skip = [type_spec.type_name]

    graphqlBody = []
    for spec_field in type_spec.field_specs:
        if spec_field.field_type in ("fk", "related_set"):
            fk_type_name = spec_field.field_type_attrs["target"]
            if fk_type_name not in skip:
                fk_type_spec = type_spec_store().get(fk_type_name)
                include_field_name = (
                    spec_field.field_type in ("fk", "related_set") and not is_top_level
                )
                if include_field_name:
                    graphqlBody.append(f"{spec_field.name} {{")
                    indent += 2
                graphqlBody.extend(
                    graphql_body(
                        fk_type_spec,
                        indent,
                        skip + [fk_type_name],
                    )
                )
                if include_field_name:
                    indent -= 2
                    graphqlBody.append(f"}}")
        else:
            graphqlBody.append(f"{spec_field.name}")

    if is_top_level:
        return " " * 10 + (os.linesep + (" " * 10)).join(graphqlBody)
    else:
        return [(" " * indent) + x for x in graphqlBody]
