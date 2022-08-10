import moonleap.resource.props as P
from moonleap import Prop, Term, create, empty_rule, extend, kebab_to_camel, rule
from moonleap.resource.forward import create_forward
from moonleap.verbs import has, provides
from titan.api_pkg.graphqlapi import GraphqlApi

from . import props
from .resources import Query

base_tags = [
    ("query", ["api-endpoint"]),
]


@create("query")
def create_query(term):
    query = Query(name=kebab_to_camel(term.data))
    return query


@rule("query", provides, "x+item~list")
def query_provides_named_item_list(query, named_item_list):
    item_list_term = Term(named_item_list.meta.term.data, named_item_list.meta.term.tag)
    return [
        create_forward(query, provides, item_list_term),
    ]


@rule("query", provides, "x+item")
def query_provides_named_item(query, named_item):
    item_term = Term(named_item.meta.term.data, named_item.meta.term.tag)
    return [
        create_forward(query, provides, item_term),
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
    named_items_provided = P.children(provides, "x+item")
    named_item_lists_provided = P.children(provides, "x+item~list")
    inputs_type_spec = Prop(props.inputs_type_spec)
    outputs_type_spec = Prop(props.outputs_type_spec)
