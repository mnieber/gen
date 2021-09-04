from moonleap import chop0
from moonleap.parser.term import word_to_term
from moonleap.resources.data_type_spec_store import FK, RelatedSet, data_type_spec_store
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


def get_endpoint_query_text(query):
    return magic_replace(
        endpoint_template,
        [
            ("endpointName", query.name),
            (
                "javaScriptArgs",
                ", ".join(R.map(ds(input_arg_to_ts_arg), query.input_args.items())),
            ),
            (
                "graphqlHeader",
                get_graphql_header(query, "query"),
            ),
            (
                "redRose",
                (os.linesep + " " * 8).join(
                    map(lambda x: f"{x}: ${x}", query.input_args.keys())
                ),
            ),
            (
                "graphqlBody",
                get_graphql_body(upper0(query.item_name)),
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
                get_graphql_header(mutation, "mutation"),
            ),
            (
                "graphqlBody",
                get_graphql_body(upper0(mutation.item_name)),
            ),
        ],
    )


def get_graphql_header(query, query_type):
    items = query.input_args.items()
    return (os.linesep + " " * 6).join(
        [
            f"{query_type} " + query.name + ("(" if items else ""),
            *map(ds(lambda n, t: "  " + input_arg_to_graphql_arg(n, t)), items),
            ") " if items else "",
        ]
    )


def get_graphql_body(type_name, indent=0, skip=None):
    if skip is None:
        skip = [type_name]

    graphqlBody = []
    spec = data_type_spec_store.get_spec(type_name)
    for spec_field in [x for x in spec.fields if not x.private]:
        if isinstance(spec_field.field_type, RelatedSet) or isinstance(
            spec_field.field_type, FK
        ):
            fk_type_name = spec_field.field_type.target
            if fk_type_name not in skip:
                graphqlBody.append(f"{spec_field.name} {{")
                graphqlBody.extend(
                    get_graphql_body(fk_type_name, indent + 2, skip + [fk_type_name])
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
