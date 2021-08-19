import moonleap.resource.props as P
from moonleap import Prop, RenderTemplates, extend, rule, tags
from moonleap.verbs import has, loads, posts
from titan.react_pkg.module import Module

from . import props
from .resources import GraphqlApi


@tags(["graphql:api"])
def create_graphql_api(term, block):
    graphql_api = GraphqlApi(name="api")
    return graphql_api


@rule("react-app", has, "api:module")
def react_app_has_api_module(react_app, api_module):
    react_app.utils_module.use_packages(["graphqlClient", "RST"])


@extend(GraphqlApi)
class ExtendGraphqlApi(RenderTemplates(__file__)):
    items_loaded = P.children(loads, "item")
    item_lists_loaded = P.children(loads, "item-list")
    forms_posted = P.children(posts, "form")
    api_module = P.parent(Module, has)
    schema_item_names = Prop(props.schema_item_names)
    sections = Prop(props.Sections)
