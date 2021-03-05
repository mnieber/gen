import moonleap.resource.props as P
from moonleap import (
    Forward,
    MemFun,
    Rel,
    add,
    extend,
    render_templates,
    rule,
    tags,
    word_to_term,
)
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config
from moonleap_tools.tool import Tool


class GraphqlApi(Tool):
    pass


@tags(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi()
    add(graphql_api, load_node_package_config(__file__))
    return graphql_api


@rule("module", has, "graphql:api")
def create_utils_module(module, graphql_api):
    return Forward(Rel(module.service.term, has, word_to_term("utils:module")))


@rule("module", has, "graphql:api")
def module_has_graphql_api(module, graphql_api):
    graphql_api.output_path = module.output_path
    module.service.utils_module.add_template_dir(__file__, "templates_utils")
    return service_has_tool_rel(module.service, graphql_api)


@extend(GraphqlApi)
class ExtendGraphqlApi:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "graphql:api")
