import moonleap.resource.props as P
import ramda as R
from moonleap import MemFun, extend, rule, tags
from moonleap.resource.rel import create_forward
from moonleap.resources.data_type_spec_store import data_type_spec_store
from moonleap.verbs import has, loads, provides
from titan.api_pkg.graphqlapi import GraphqlApi

from . import props
from .resources import Query


@tags(["query"])
def create_query(term, block):
    query = Query(name=term.data)
    return query


@rule("graphql:api", loads, "item")
def graphql_api_loads_item(graphql_api, item):
    return [create_forward(graphql_api, has, f"get-{item.item_name}:query")]


@rule("graphql:api", loads, "item")
def query_provides_item(graphql_api, item):
    query = R.find(lambda x: x.name == f"get-{item.item_name}")(graphql_api.queries)
    data_type = data_type_spec_store.get_spec(item.item_name)
    query.data_type_inputs = data_type
    query.fields = data_type.query_item_by
    query.data_type_output = data_type

    return [create_forward(query, provides, f"{item.item_name}:item", obj_res=item)]


@rule("graphql:api", loads, "item-list")
def graphql_api_loads_item_list(graphql_api, item_list):
    return [create_forward(graphql_api, has, f"get-{item_list.item_name}-list:query")]


@rule("graphql:api", loads, "item-list")
def query_provides_item_list(graphql_api, item_list):
    query = R.find(lambda x: x.name == f"get-{item_list.item_name}-list")(
        graphql_api.queries
    )
    data_type = data_type_spec_store.get_spec(item_list.item_name)
    query.data_type_inputs = data_type
    query.fields = data_type.query_item_list_by
    query.data_type_output = data_type
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
