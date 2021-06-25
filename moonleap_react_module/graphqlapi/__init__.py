import moonleap.resource.props as P
from moonleap import MemFun, add, create_forward, extend, render_templates, rule, tags
from moonleap.utils.inflect import plural
from moonleap.verbs import has, provides
from moonleap_project.service import Service
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import GraphqlApi


@tags(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi(name="api")
    graphql_api.output_path = "api"
    add(graphql_api, load_node_package_config(__file__))
    return graphql_api


@rule("graphql:api", provides, "item-list")
def api_provides_item_list(api, item_list):
    load_items_effect = f"{plural(item_list.item_name)}:load-items-effect"
    return create_forward(api.module.term, has, load_items_effect)


@rule("service", has, "graphql:api")
def create_utils_module(service, graphql_api):
    graphql_api.output_paths.add_source(service)
    service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(GraphqlApi)
class ExtendGraphqlApi:
    render = MemFun(render_templates(__file__))
    item_lists = P.children(provides, "item-list")
    provides_item_list = MemFun(props.provides_item_list)


@extend(Service)
class ExtendService:
    graphql_api = P.child(has, "graphql:api")
