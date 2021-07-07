import moonleap.resource.props as P
from moonleap import add, extend, kebab_to_camel, tags
from moonleap.verbs import has
from moonleap_project.service import Service
from moonleap_react.nodepackage import load_node_package_config

from .resources import ApiModule  # noqa


@tags(["api:module"])
def create_app_module(term, block):
    module = ApiModule(name=kebab_to_camel(term.data))
    module.output_path = f"src/{module.name}"
    add(module, load_node_package_config(__file__))
    return module


@extend(ApiModule)
class ExtendApiModule:
    load_item_effects = P.children(has, "load-item-effect")
    load_items_effects = P.children(has, "load-items-effect")
    graphql_api = P.child(has, "graphql:api")


@extend(Service)
class ExtendService:
    api_module = P.child(has, "api:module")
