from moonleap import MemFun, Prop, create, extend

from . import props
from .resources import GraphqlApi


@create("graphql:api")
def create_graphql_api(term, block):
    graphql_api = GraphqlApi()
    return graphql_api


@extend(GraphqlApi)
class ExtendGraphqlApi:
    item_types = Prop(props.item_types)
    mutations_that_post_item = MemFun(props.mutations_that_post_item)
