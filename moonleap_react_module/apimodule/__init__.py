import moonleap.resource.props as P
from moonleap import add, extend, kebab_to_camel, tags
from moonleap.verbs import has
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
    load_items_effects = P.children(has, "load-items-effect")
