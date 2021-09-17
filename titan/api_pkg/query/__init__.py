import moonleap.resource.props as P
import ramda as R
from moonleap import MemFun, Prop, create, extend, kebab_to_camel, rule, upper0
from moonleap.resource.rel import create_forward
from moonleap.utils.inflect import plural
from moonleap.verbs import has, loads, provides
from titan.api_pkg.graphqlapi import GraphqlApi

from . import props
from .resources import Query


@create(["query"])
def create_query(term, block):
    name = kebab_to_camel(term.data)
    query = Query(name=name, fun_name=kebab_to_camel(term.data))
    return query


@rule("graphql:api", loads, "item")
def graphql_api_loads_item(graphql_api, item):
    return [create_forward(graphql_api, has, f"{item.item_name}:query")]


@rule("graphql:api", loads, "item")
def create_get_item_query(graphql_api, item):
    query_name = f"{kebab_to_camel(item.item_name)}"
    query = R.find(lambda x: x.name == query_name)(graphql_api.queries)
    query.fun_name = f"get{upper0(query_name)}"
    assert query
    return [create_forward(query, provides, f"{item.item_name}:item", obj_res=item)]


@rule("graphql:api", loads, "item-list")
def graphql_api_loads_item_list(graphql_api, item_list):
    return [create_forward(graphql_api, has, f"{plural(item_list.item_name)}:query")]


@rule("graphql:api", loads, "item-list")
def create_get_items_query(graphql_api, item_list):
    query_name = f"{kebab_to_camel(plural(item_list.item_name))}"
    query = R.find(lambda x: x.name == query_name)(graphql_api.queries)
    query.fun_name = f"get{upper0(query_name)}"
    assert query
    return [
        create_forward(
            query, provides, f"{item_list.item_name}:item-list", obj_res=item_list
        )
    ]


empty_rules = [
    ("graphql:api", has, "query"),
    ("query", provides, "item"),
    ("query", provides, "item-list"),
]


@extend(GraphqlApi)
class ExtendGraphqlApi:
    queries = P.children(has, "query")


@extend(Query)
class ExtendQuery:
    items_provided = P.children(provides, "item")
    item_lists_provided = P.children(provides, "item-list")
    provides_item = MemFun(props.provides_item)
    provides_item_list = MemFun(props.provides_item_list)
    inputs_type_spec = Prop(props.inputs_type_spec)
    outputs_type_spec = Prop(props.outputs_type_spec)
