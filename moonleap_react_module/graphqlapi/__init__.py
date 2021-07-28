import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, extend, render_templates, rule, tags
from moonleap.verbs import has, loads, posts
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import GraphqlApi


@tags(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi(name="api")
    add(graphql_api, load_node_package_config(__file__))
    return graphql_api


@rule("react-app", has, "api:module")
def react_app_has_api_module(react_app, api_module):
    react_app.utils_module.add_template_dir(__file__, "templates_utils")
    react_app.app_module.add_template_dir(__file__, "templates_appstore")


@extend(GraphqlApi)
class ExtendGraphqlApi:
    render = MemFun(render_templates(__file__))
    items_loaded = P.children(loads, "item")
    item_lists_loaded = P.children(loads, "item-list")
    forms_posted = P.children(posts, "form")
    api_module = P.parent(Module, has)
    schema_item_names = Prop(props.schema_item_names)
    p_section_load_item_effect = MemFun(props.p_section_load_item_effect)
    p_section_item_fields = MemFun(props.p_section_item_fields)
    p_section_post_form = MemFun(props.p_section_post_form)
