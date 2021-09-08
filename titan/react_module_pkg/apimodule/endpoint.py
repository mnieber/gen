import os

import ramda as R
from moonleap import chop0
from moonleap.parser.term import word_to_term
from moonleap.resources.data_type_spec_store import data_type_spec_store
from moonleap.utils.case import kebab_to_camel, upper0
from moonleap.utils.fp import ds
from moonleap.utils.inflect import plural
from moonleap.utils.magic_replace import magic_replace
from titan.api_pkg.mutation.data_types import default_mutation_output_data_type

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


def _fields(query):
    fields = {}
    for field_name in query.fields or query.data_type_in.field_by_name.keys():
        data_type_field = query.data_type_in.field_by_name[field_name]
        fields[field_name] = data_type_field.type
    return fields


def _javascript_args(query):
    return ", ".join(R.map(ds(input_arg_to_ts_arg), _fields(query).items()))


def get_endpoint_query_text(query):
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
                (os.linesep + " " * 8).join(map(lambda x: f"{x}: ${x}", query.fields)),
            ),
            (
                "graphqlBody",
                _graphql_body(query.data_type_out),
            ),
            ("blueDaisy", (os.linesep + " " * 8).join(query.input_args.keys())),
            ("purpleOrchid", get_graphql_response(query)),
        ],
    )


def get_endpoint_mutation_text(mutation):
    return magic_replace(
        endpoint_template,
        [
            ("endpointName", mutation.name),
            ("javaScriptArgs", ", ".join(mutation.input_args.keys())),
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
    items = _fields(query).items()
    return (os.linesep + " " * 6).join(
        [
            f"{query_type} " + query.name + ("(" if items else ""),
            *map(ds(lambda n, t: "  " + input_arg_to_graphql_arg(n, t)), items),
            ") " if items else "",
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


def input_type_to_ts_type(arg_type):
    if arg_type == "string":
        return "string"

    term = word_to_term(arg_type)

    if term and term.tag == "item":
        return f"{upper0(kebab_to_camel(term.data))}T"

    raise Exception(f"Cannot deduce typescript type for {arg_type}")


def input_arg_to_ts_arg(arg_name, arg_type):
    ts_type = input_type_to_ts_type(arg_type)
    return f"{arg_name}: {ts_type}"


def input_arg_to_graphql_arg(arg_name, arg_type):
    graphql_type = input_type_to_graphql_type(arg_type)

    return f"${arg_name}: {graphql_type}"


def input_type_to_graphql_type(arg_type):
    if arg_type == "string":
        return "String"

    term = word_to_term(arg_type)

    if term and term.tag == "item":
        return f"{upper0(kebab_to_camel(term.data))}Type"

    raise Exception(f"Cannot deduce graphql type for {arg_type}")


def get_graphql_response(query):
    if query.is_list:
        return f"normalize(response.{query.name}, {plural(query.item_name)}).entities"
    else:
        return f"normalize(response.{query.name}, {query.item_name}).entities"
