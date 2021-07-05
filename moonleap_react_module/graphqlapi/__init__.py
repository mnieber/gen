import moonleap.resource.props as P
from moonleap import (MemFun, add, create_forward, extend, render_templates,
                      rule, tags)
from moonleap.utils.inflect import plural
from moonleap.verbs import has, provides
from moonleap_project.service import Service
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import GraphqlApi


@tags(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi(name="api")
    add(graphql_api, load_node_package_config(__file__))
    return graphql_api


@rule("graphql:api", provides, "item-list")
def api_provides_item_list(api, item_list):
    load_items_effect = f"{plural(item_list.item_name)}:load-items-effect"
    return create_forward(api.module.term, has, load_items_effect)


@rule("service", has, "api:module")
def service_has_api_module(service, api_module):
    service.utils_module.add_template_dir(__file__, "templates_utils")
    service.app_module.add_template_dir(__file__, "templates_appstore")


@extend(GraphqlApi)
class ExtendGraphqlApi:
    render = MemFun(render_templates(__file__))
    item_lists = P.children(provides, "item-list")
    provides_item_list = MemFun(props.provides_item_list)
    api_module = P.parent(Module, has)


@extend(Service)
class ExtendService:
    api_module = P.child(has, "api:module")
