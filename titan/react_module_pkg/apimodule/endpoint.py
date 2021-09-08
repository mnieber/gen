import os

import ramda as R
from moonleap import chop0
from moonleap.parser.term import word_to_term
from moonleap.resources.data_type_spec_store import data_type_spec_store
from moonleap.utils.case import kebab_to_camel, upper0
from moonleap.utils.fp import ds
from moonleap.utils.inflect import plural
from moonleap.utils.magic_replace import magic_replace

endpoint_template = chop0(
    """
  endpointName(
    javaScriptArgs
  ) {
    return this._doQuery(
      'endpointName',
      `graphqlHeader{
        endpointName(
          redRose
        ) {
          graphqlBody
        }
      }`,
      {
          blueDaisy
      },
      (response: ObjT) => purpleOrchid,
      (error: ObjT) => error.response.errors[0].message
    );
  }
"""
)


def _input_fields(query):
    fields = {}
    for field_name in getattr(query, "fields", []) or (
        query.data_type_in.field_by_name.keys() if query.data_type_in else []
    ):
        data_type_field = query.data_type_in.field_by_name[field_name]
        fields[field_name] = data_type_field
    return fields


def _javascript_args(query):
    return ", ".join(R.map(ds(_input_field_to_ts_arg), _input_fields(query).items()))


def get_endpoint_query_text(query):
    field_names = _input_fields(query).keys()

    return magic_replace(
        endpoint_template,
        [
            ("endpointName", query.name),
            (
                "javaScriptArgs",
                _javascript_args(query),
            ),
            (
                "graphqlHeader",
                _graphql_header(query, "query"),
            ),
            (
                "redRose",
                (os.linesep + " " * 8).join(map(lambda x: f"{x}: ${x}", field_names)),
            ),
            (
                "graphqlBody",
                _graphql_body(query.data_type_out),
            ),
            ("blueDaisy", (os.linesep + " " * 8).join(field_names)),
            ("purpleOrchid", get_graphql_response(query, is_list=True)),
        ],
    )


def get_endpoint_mutation_text(mutation):
    return magic_replace(
        endpoint_template,
        [
            ("endpointName", mutation.name),
            (
                "javaScriptArgs",
                _javascript_args(mutation),
            ),
            (
                "graphqlHeader",
                _graphql_header(mutation, "mutation"),
            ),
            (
                "graphqlBody",
                _graphql_body(mutation.data_type_out),
            ),
        ],
    )


def _graphql_header(query, query_type):
    input_fields = _input_fields(query).items()
    return (os.linesep + " " * 6).join(
        [
            f"{query_type} " + query.name + ("(" if input_fields else ""),
            *map(
                ds(lambda n, t: "  " + _input_field_to_graphql_arg(n, t)), input_fields
            ),
            ") " if input_fields else "",
        ]
    )


def _graphql_body(spec, indent=0, skip=None):
    if skip is None:
        skip = [spec.type_name]

    graphqlBody = []
    for spec_field in [x for x in spec.field_by_name.values() if not x.private]:
        if spec_field.field_type in ("fk", "related_set"):
            fk_type_name = spec_field.field_type_attrs["target"]
            if fk_type_name not in skip:
                graphqlBody.append(f"{spec_field.name} {{")
                graphqlBody.extend(
                    _graphql_body(
                        data_type_spec_store.get_spec(fk_type_name),
                        indent + 2,
                        skip + [fk_type_name],
                    )
                )
                graphqlBody.append(f"}}")  # noqa: F541
        else:
            graphqlBody.append(f"{spec_field.name}")

    if indent == 0:
        return (os.linesep + (" " * 10)).join(graphqlBody)
    else:
        return [(" " * indent) + x for x in graphqlBody]


def _input_field_to_ts_type(input_field):
    if input_field.field_type in ("string", "json", "url"):
        return "string"

    if input_field.field_type in ("bool",):
        return "bool"

    if input_field.field_type in ("fk",):
        return f"{upper0(kebab_to_camel(input_field.field_type_attrs['target']))}T"

    raise Exception(f"Cannot deduce typescript type for {input_field.field_type}")


def _input_field_to_ts_arg(arg_name, input_field):
    ts_type = _input_field_to_ts_type(input_field)
    return f"{arg_name}: {ts_type}"


def _input_field_to_graphql_arg(arg_name, input_field):
    graphql_type = _input_field_to_graphql_type(input_field)

    return f"${arg_name}: {graphql_type}"


def _input_field_to_graphql_type(input_field):
    if input_field.field_type in ("string", "json", "url"):
        return "String"

    if input_field.field_type in ("bool",):
        return "Boolean"

    if input_field.field_type in ("fk",):
        return f"{upper0(kebab_to_camel(input_field.field_type_attrs['target']))}Type"

    raise Exception(f"Cannot deduce graphql type for {input_field.field_type}")


def get_graphql_response(query, is_list):
    # TODO: return normalized data based on query.items_provided and query.item_lists_provided
    if is_list:
        return (
            f"normalize(response.{plural(query.name)}, {plural(query.name)}).entities"
        )
    else:
        return f"normalize(response.{query.name}, {query.name}).entities"
