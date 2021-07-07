import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, extend, render_templates, rule, tags
from moonleap.verbs import has, loads
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import GraphqlApi


@tags(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi(name="api")
    add(graphql_api, load_node_package_config(__file__))
    return graphql_api


@rule("service", has, "api:module")
def service_has_api_module(service, api_module):
    service.utils_module.add_template_dir(__file__, "templates_utils")
    service.app_module.add_template_dir(__file__, "templates_appstore")


@extend(GraphqlApi)
class ExtendGraphqlApi:
    render = MemFun(render_templates(__file__))
    items = P.children(loads, "item")
    item_lists = P.children(loads, "item-list")
    api_module = P.parent(Module, has)
    item_names = Prop(props.item_names)
