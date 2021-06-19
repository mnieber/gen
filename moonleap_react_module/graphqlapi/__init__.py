import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    add,
    create_forward,
    extend,
    render_templates,
    rule,
    tags,
)
from moonleap.verbs import has
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config
from moonleap_react_module.api import Api

from . import props


class GraphqlApi(Api):
    pass


@tags(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi(name="api")
    graphql_api.output_path = "api"
    add(graphql_api, load_node_package_config(__file__))
    return graphql_api


@rule("service", has, "graphql:api")
def create_utils_module(service, graphql_api):
    graphql_api.output_paths.add_source(service)


@rule("service", has, "graphql:api")
def add_templates_utils(service, graphql_api):
    service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(GraphqlApi)
class ExtendGraphqlApi:
    render = MemFun(render_templates(__file__))
    construct_item_list_section = MemFun(props.construct_item_list_section)
    item_list_io_section = MemFun(props.item_list_io_section)
    import_api_section = Prop(props.import_api_section)


@extend(Module)
class ExtendModule:
    graphql_api = P.child(has, "graphql:api")
