import moonleap.resource.props as P
from moonleap_react.module import Module
from moonleap_react.utilsmodule import create_utils_module
from moonleap_tools.tool import Tool
from moonleap import MemFun, add, extend, render_templates, rule, tags
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
    utils_module = create_utils_module(module.service)
    utils_module.add_template_dir(__file__, "templates_utils")


@extend(GraphqlApi)
class ExtendGraphqlApi:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "graphql:api")
