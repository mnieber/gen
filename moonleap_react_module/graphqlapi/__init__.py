import moonleap.resource.props as P
from moonleap import (
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
from moonleap_react.module import Module
from moonleap_tools.tool import Tool

from . import node_package_configs


class GraphqlApi(Tool):
    pass


@tags(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi()
    add(graphql_api, node_package_configs.get())
    return graphql_api


@rule("module", has, "graphql:api")
def create_utils_module(module, graphql_api):
    return Rel(module.service.term, has, word_to_term("utils:module"))


@rule("module", has, "graphql:api")
def module_has_graphql_api(module, graphql_api):
    module.add_component(graphql_api)
    module.service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(GraphqlApi)
class ExtendGraphqlApi:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "graphql:api")
