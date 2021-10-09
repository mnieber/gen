import moonleap.resource.props as P
from moonleap import create_forward, extend, feeds, receives, rule
from moonleap.verbs import has, shows
from titan.react_pkg.module import Module

rules = [
    (("module", has, "component"), receives("node_package_configs")),
    (("module", has, "component"), receives("react_app_configs")),
    (("module", has, "component"), feeds("output_paths")),
]


@rule("module", shows, "component")
def module_shows_component(module, component):
    if not component.module:
        return create_forward(module, has, component)


@extend(Module)
class ExtendModule:
    routed_components = P.children(shows, "component")
