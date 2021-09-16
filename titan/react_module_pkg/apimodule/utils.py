import os

import ramda as R
from moonleap import kebab_to_camel, upper0
from moonleap.resources.type_spec_store import type_spec_store
from moonleap.utils.fp import ds


def javascript_args(type_spec):
    field_specs = type_spec.field_spec_by_name.items()
    return ", ".join(R.map(ds(_field_spec_to_ts_arg), field_specs))


def _field_spec_to_ts_type(field_spec):
    if field_spec.field_type in ("string", "json", "url"):
        return "string"

    if field_spec.field_type in ("bool",):
        return "bool"

    if field_spec.field_type in ("fk",):
        return f"{upper0(kebab_to_camel(field_spec.field_type_attrs['target']))}T"

    raise Exception(f"Cannot deduce typescript type for {field_spec.field_type}")


def _field_spec_to_ts_arg(field_name, field_spec):
    ts_type = _field_spec_to_ts_type(field_spec)
    return f"{field_name}: {ts_type}"


def _input_field_to_graphql_type(field_spec):
    if field_spec.field_type in ("string", "json", "url"):
        return "String"

    if field_spec.field_type in ("bool",):
        return "Boolean"

    if field_spec.field_type in ("fk",):
        return f"{upper0(kebab_to_camel(field_spec.field_type_attrs['target']))}Type"

    raise Exception(f"Cannot deduce graphql type for {field_spec.field_type}")


def field_spec_to_graphql_arg(field_name, field_spec, before):
    graphql_type = _input_field_to_graphql_type(field_spec)
    if before:
        return f"${field_name}: {graphql_type}"
    return f"{field_name}: ${field_name}"


def graphql_body(type_spec, indent=0, skip=None):
    if skip is None:
        skip = [type_spec.type_name]

    graphqlBody = []
    for spec_field in type_spec.field_spec_by_name.values():
        if spec_field.field_type in ("fk", "related_set"):
            fk_type_name = spec_field.field_type_attrs["target"]
            if fk_type_name not in skip:
                fk_type_spec = type_spec_store.get(fk_type_name)
                graphqlBody.append(f"{spec_field.name} {{")
                graphqlBody.extend(
                    graphql_body(
                        fk_type_spec,
                        indent + 2,
                        skip + [fk_type_name],
                    )
                )
                graphqlBody.append(f"}}")  # noqa: F541
        else:
            graphqlBody.append(f"{spec_field.name}")

    if indent == 0:
        return " " * 10 + (os.linesep + (" " * 10)).join(graphqlBody)
    else:
        return [(" " * indent) + x for x in graphqlBody]
