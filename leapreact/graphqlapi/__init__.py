from leaptools.tool import Tool
from moonleap import add, extend, render_templates, rule, tags
from moonleap.verbs import has

from . import node_package_configs


class GraphqlApi(Tool):
    pass


@tags(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi()
    add(graphql_api, node_package_configs.get())
    return graphql_api


@rule("module", has, "graphql:api")
def module_has_graphql_api(module, graphql_api):
    module.add_component(graphql_api)


@extend(GraphqlApi)
class ExtendGraphqlApi:
    render = render_templates(__file__)
