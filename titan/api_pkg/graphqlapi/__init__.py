from moonleap import MemFun, create, extend

from . import props
from .resources import GraphqlApi


@create("graphql:api")
def create_graphql_api(term):
    graphql_api = GraphqlApi()
    return graphql_api


@extend(GraphqlApi)
class ExtendGraphqlApi:
    mutations_that_post_item = MemFun(props.mutations_that_post_item)
