import moonleap.resource.props as P
from moonleap import add, extend, kebab_to_camel, tags
from moonleap.verbs import has
from titan.react_pkg.nodepackage import load_node_package_config
from titan.react_pkg.reactapp import ReactApp

from .resources import ApiModule  # noqa


@tags(["api:module"])
def create_api_module(term, block):
    module = ApiModule(name=kebab_to_camel(term.data))
    module.output_path = f"src/{module.name}"
    add(module, load_node_package_config(__file__))
    return module


@extend(ApiModule)
class ExtendApiModule:
    load_item_effects = P.children(has, "load-item-effect")
    load_items_effects = P.children(has, "load-items-effect")
    graphql_api = P.child(has, "graphql:api")


@extend(ReactApp)
class ExtendReactApp:
    api_module = P.child(has, "api:module")
