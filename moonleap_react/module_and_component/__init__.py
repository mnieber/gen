import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has, shows
from moonleap_react.component import Component
from moonleap_react.module import Module


@rule("module", has, "*", fltr_obj=P.fltr_instance(Component))
def module_has_component(module, component):
    module.node_package_configs.add_source(component)
    component.output_paths.add_source(module)


@rule("module", shows, "*", fltr_obj=P.fltr_instance(Component))
def module_shows_component(module, component):
    module_has_component(module, component)
    module.add_to_routed_components(component)


@extend(Module)
class ExtendModule:
    routed_components = P.children(shows, "component")
