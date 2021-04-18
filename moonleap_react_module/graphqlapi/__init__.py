from moonleap import MemFun, add, create_forward, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_react.component import Component
from moonleap_react.nodepackage import load_node_package_config


class GraphqlApi(Component):
    pass


@tags(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi(name="api")
    add(graphql_api, load_node_package_config(__file__))
    return graphql_api


@rule("module", has, "graphql:api")
def create_utils_module(module, graphql_api):
    return create_forward(module.service, has, "utils:module")


@rule("module", has, "graphql:api")
def module_has_graphql_api(module, graphql_api):
    module.service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(GraphqlApi)
class ExtendGraphqlApi:
    render = MemFun(render_templates(__file__))
