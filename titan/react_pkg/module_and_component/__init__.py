import moonleap.resource.props as P
from moonleap import create_forward, extend, rule
from moonleap.verbs import has, shows
from titan.react_pkg.module import Module


@rule("module", has, "component")
def module_has_component(module, component):
    module.node_package_configs.add_source(component)
    module.react_app_configs.add_source(component)
    component.output_paths.add_source(module)


@rule("module", shows, "component")
def module_shows_component(module, component):
    return create_forward(module, has, component._meta.term)


@extend(Module)
class ExtendModule:
    routed_components = P.children(shows, "component")
