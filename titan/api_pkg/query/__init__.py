import moonleap.resource.props as P
import ramda as R
from moonleap import MemFun, Prop, extend, kebab_to_camel, rule, tags, upper0
from moonleap.resource.rel import create_forward
from moonleap.resources.type_spec_store import type_spec_store
from moonleap.verbs import has, loads, provides
from titan.api_pkg.graphqlapi import GraphqlApi

from . import props
from .resources import Query


@tags(["query"])
def create_query(term, block):
    name = kebab_to_camel(term.data)
    query = Query(name=name)
    return query


@rule("graphql:api", loads, "item")
def graphql_api_loads_item(graphql_api, item):
    return [create_forward(graphql_api, has, f"get-{item.item_name}:query")]


@rule("graphql:api", loads, "item")
def create_get_item_query(graphql_api, item):
    query_name = f"get{kebab_to_camel(upper0(item.item_name))}"
    query = R.find(lambda x: x.name == query_name)(graphql_api.queries)
    return [create_forward(query, provides, f"{item.item_name}:item", obj_res=item)]


@rule("graphql:api", loads, "item-list")
def graphql_api_loads_item_list(graphql_api, item_list):
    return [create_forward(graphql_api, has, f"get-{item_list.item_name}-list:query")]


@rule("graphql:api", loads, "item-list")
def create_get_items_query(graphql_api, item_list):
    query_name = f"get{kebab_to_camel(upper0(item_list.item_name))}List"
    query = R.find(lambda x: x.name == query_name)(graphql_api.queries)
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
