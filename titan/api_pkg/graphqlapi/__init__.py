from moonleap import MemFun, Prop, create, extend

from . import props
from .resources import GraphqlApi


@create(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi()
    return graphql_api


@extend(GraphqlApi)
class ExtendGraphqlApi:
    types = Prop(props.types)
    queries_that_provide_item = MemFun(props.queries_that_provide_item)
    queries_that_provide_item_list = MemFun(props.queries_that_provide_item_list)
