import os
import typing as T
from dataclasses import dataclass, field

import ramda as R
from moonleap import chop0, get_session, upper0
from moonleap.parser.term import word_to_term
from moonleap.resources.data_type_spec_store import FK, RelatedSet, data_type_spec_store
from moonleap.utils.case import kebab_to_camel
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


def get_graphql_response(query):
    if query.out_item:
        return f"normalize(response.{query.name}, {query.out_item}).entities"

    if query.out_item_list:
        return f"normalize(response.{query.name}, {query.out_item_list}List).entities"

    raise Exception(f"Cannot deduce response for query {query.name}")


def get_graphql_header(query, query_type):
    items = query.input_args.items()
    return (os.linesep + " " * 6).join(
        [
            f"{query_type} " + query.name + ("(" if items else ""),
            *map(ds(lambda n, t: "  " + input_arg_to_graphql_arg(n, t)), items),
            ") " if items else "",
        ]
    )


def input_arg_to_graphql_arg(arg_name, arg_type):
    graphql_type = input_type_to_graphql_type(arg_type)

    return f"${arg_name}: {graphql_type}"


def input_arg_to_ts_arg(arg_name, arg_type):
    ts_type = input_type_to_ts_type(arg_type)
    return f"{arg_name}: {ts_type}"


def input_type_to_ts_type(arg_type):
    if arg_type == "string":
        return "string"

    term = word_to_term(arg_type)

    if term and term.tag == "item":
        return f"{upper0(kebab_to_camel(term.data))}T"

    raise Exception(f"Cannot deduce typescript type for {arg_type}")


def input_type_to_graphql_type(arg_type):
    if arg_type == "string":
        return "String"

    term = word_to_term(arg_type)

    if term and term.tag == "item":
        return f"{upper0(kebab_to_camel(term.data))}Type"

    raise Exception(f"Cannot deduce graphql type for {arg_type}")


@dataclass
class Endpoint:
    name: str
    input_args: dict = field(default_factory=dict)
    out_item: T.Any = None
    out_item_list: T.Any = None


def add_output_to_endpoint(items, item_lists, output_value, endpoint):
    term = word_to_term(output_value)
    if term is None:
        raise Exception(f"Could not parse output value {output_value}")

    item_name = kebab_to_camel(term.data)

    if term.tag == "item":
        endpoint.out_item = item_name
        items.append(item_name)

    if term.tag == "item-list":
        endpoint.out_item_list = item_name
        item_lists.append(item_name)


def add_input_args_to_endpoint(input_values, endpoint):
    for input_value in input_values:
        term = word_to_term(input_value)
        if term is None:
            endpoint.input_args[input_value] = "string"
        else:
            endpoint.input_args[f"{input_value.data}_{input_value.tag}"] = upper0(
                kebab_to_camel(term.data)
            )


def get_queries(res):
    queries = []
    items = []
    item_lists = []

    query_dicts = get_session().settings.get("queries", {})
    for endpoint_name, query_dict in query_dicts.items():
        query = Endpoint(name=kebab_to_camel(endpoint_name))
        queries.append(query)
        add_input_args_to_endpoint(query_dict.get("in", []), query)
        add_output_to_endpoint(items, item_lists, query_dict["out"], query)

    for item_loaded in res.items_loaded:
        if item_loaded.item_name not in items:
            query = Endpoint(name=f"get{upper0(item_loaded.item_name)}")
            query.out_item = item_loaded.item_name
            queries.append(query)

    for item_list_loaded in res.item_lists_loaded:
        if item_list_loaded.item_name not in item_lists:
            query = Endpoint(name=f"get{upper0(plural(item_list_loaded.item_name))}")
            query.out_item_list = item_list_loaded.item_name
            queries.append(query)

    return queries


def get_mutations(res):
    mutations = []
    items = []
    item_lists = []

    mutation_dicts = get_session().settings.get("mutations", {})

    for endpoint_name, mutation_dict in mutation_dicts.items():
        mutation = Endpoint(name=kebab_to_camel(endpoint_name))
        mutations.append(mutation)
        add_output_to_endpoint(items, item_lists, mutation_dict["out"], mutation)
        add_input_args_to_endpoint(mutation_dict.get("in", []), mutation)

    for form_posted in res.forms_posted:
        mutation_name = f"post{upper0(form_posted.name)}"
        if not [m for m in mutations if m.name == mutation_name]:
            mutation = Endpoint(name=mutation_name)
            mutations.append(mutation)

    for item_posted in res.items_posted:
        mutation_name = f"post{upper0(item_posted.item_name)}"
        if not [m for m in mutations if m.name == mutation_name]:
            mutation = Endpoint(name=mutation_name)
            mutations.append(mutation)

    return mutations


def schema_item_names(queries, mutations):
    result = []
    for endpoint in [*queries, *mutations]:
        if endpoint.out_item:
            result.append(endpoint.out_item)
        if endpoint.out_item_list:
            result.append(endpoint.out_item_list)
    return R.uniq(result)


def get_graphql_body(type_name, indent=0, skip=None):
    if skip is None:
        skip = [type_name]

    graphqlBody = []
    spec = data_type_spec_store.get_spec(type_name)
    for field in [x for x in spec.fields if not x.private]:
        if isinstance(field.field_type, RelatedSet) or isinstance(field.field_type, FK):
            fk_type_name = field.field_type.target
            if fk_type_name not in skip:
                graphqlBody.append(f"{field.name} {{")
                graphqlBody.extend(
                    get_graphql_body(fk_type_name, indent + 2, skip + [fk_type_name])
                )
                graphqlBody.append(f"}}")
        else:
            graphqlBody.append(f"{field.name}")

    if indent == 0:
        return (os.linesep + (" " * 10)).join(graphqlBody)
    else:
        return [(" " * indent) + x for x in graphqlBody]


class Sections:
    def __init__(self, res):
        self.res = res

    def schemas(self):
        result = []
        queries = get_queries(self.res)
        mutations = get_mutations(self.res)

        for item_name in schema_item_names(queries, mutations):
            result.append(
                f"const {item_name} = new schema.Entity('{plural(item_name)}');"
            )
            if [q for q in queries if item_name == q.out_item_list]:
                result.append(
                    f"const {item_name}List = new schema.Array('{item_name}');"
                )

        return os.linesep.join(result)

    def queries(self):
        result = []
        queries = get_queries(self.res)

        for query in queries:
            text = magic_replace(
                endpoint_template,
                [
                    ("endpointName", query.name),
                    (
                        "javaScriptArgs",
                        ", ".join(
                            R.map(ds(input_arg_to_ts_arg), query.input_args.items())
                        ),
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
                        get_graphql_body(upper0(query.out_item_list or query.out_item)),
                    ),
                    ("blueDaisy", (os.linesep + " " * 8).join(query.input_args.keys())),
                    ("purpleOrchid", get_graphql_response(query)),
                ],
            )
            result.append(text)

        return os.linesep.join(result)

    def mutations(self):
        result = []
        mutations = get_mutations(self.res)

        for mutation in mutations:
            text = magic_replace(
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
                        get_graphql_body(mutation.out_item_list or mutation.out_item),
                    ),
                ],
            )
            result.append(text)

        return os.linesep.join(result)
