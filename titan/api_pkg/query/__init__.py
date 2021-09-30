import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    create,
    empty_rule,
    extend,
    kebab_to_camel,
    kebab_to_snake,
    rule,
)
from moonleap.resource.forward import create_forward
from moonleap.utils.inflect import plural
from moonleap.verbs import has, loads, provides
from titan.api_pkg.graphqlapi import GraphqlApi
from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList

from . import props
from .resources import Query


@create("query")
def create_query(term, block):
    name = kebab_to_camel(term.data)
    query = Query(
        name=name,
        name_snake=kebab_to_snake(term.data),
        fun_name=kebab_to_camel(term.data),
    )
    return query


@rule("graphql:api", loads, "item")
def graphql_api_loads_item(graphql_api, item):
    query_term_str = f"get-{item.item_name}:query"
    return [
        create_forward(graphql_api, has, query_term_str),
        create_forward(query_term_str, provides, f"{item.item_name}:item"),
    ]


@rule("graphql:api", loads, "item~list")
def graphql_api_loads_item_list(graphql_api, item_list):
    query_term_str = f"get-{plural(item_list.item_name)}:query"
    return [
        create_forward(graphql_api, has, query_term_str),
        create_forward(query_term_str, provides, f"{item_list.item_name}:item~list"),
    ]


rules = [
    (("graphql:api", has, "query"), empty_rule()),
    (("query", provides, "item"), empty_rule()),
    (("query", provides, "item~list"), empty_rule()),
]


@extend(GraphqlApi)
class ExtendGraphqlApi:
    queries = P.children(has, "query")


@extend(Query)
class ExtendQuery:
    items_provided = P.children(provides, "item")
    item_lists_provided = P.children(provides, "item~list")
    inputs_type_spec = Prop(props.inputs_type_spec)
    outputs_type_spec = Prop(props.outputs_type_spec)


@extend(Item)
class ExtendItem:
    provider_queries = P.parents("query", provides)


@extend(ItemList)
class ExtendItemList:
    provider_queries = P.parents("query", provides)
