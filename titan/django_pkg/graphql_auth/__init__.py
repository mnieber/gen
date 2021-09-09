from moonleap import add, extend, create
from titan.project_pkg.service import Tool
from titan.tools_pkg.pipdependency import PipRequirement

from . import django_configs


class GraphqlAuth(Tool):
    pass


@create(["graphql-auth"])
def create_graphql_auth(term, block):
    graphql_auth = GraphqlAuth(name="graphql-auth")
    add(graphql_auth, django_configs.get())
    add(
        graphql_auth,
        PipRequirement(["django-rtk-green"]),
    )
    return graphql_auth


@extend(GraphqlAuth)
class ExtendGraphqlAuth:
    pass
