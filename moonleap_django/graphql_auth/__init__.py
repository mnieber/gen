import moonleap.resource.props as P
from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import uses
from moonleap_project.service import Tool

from . import django_configs


class GraphqlAuth(Tool):
    pass


@tags(["graphql-auth"])
def create_graphql_auth(term, block):
    graphql_auth = GraphqlAuth(name="graphql-auth")
    add(graphql_auth, django_configs.get())
    return graphql_auth


@rule("service", uses, "graphql-auth")
def service_uses_graphql_auth(service, graphql_auth):
    pass


@extend(GraphqlAuth)
class ExtendGraphqlAuth:
    pass
    # render = MemFun(render_templates(__file__))
