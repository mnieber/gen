import moonleap.resource.props as P
from moonleap import MemFun, Prop, create, create_forward, empty_rule, extend, rule
from moonleap.verbs import has

from . import props
from .resources import GraphqlApi

rules = [(("graphql:api", has, "type-registry"), empty_rule())]


@create("graphql:api")
def create_graphql_api(term):
    graphql_api = GraphqlApi()
    return graphql_api


@rule("graphql:api")
def graphql_api_created(graphql_api):
    return create_forward(graphql_api, has, ":type-registry")


@extend(GraphqlApi)
class ExtendGraphqlApi:
    type_reg = P.child(has, "type-registry")
    mutations_that_post_item = MemFun(props.mutations_that_post_item)
