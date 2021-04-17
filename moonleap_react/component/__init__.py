import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from moonleap_react.nodepackage import StoreNodePackageConfigs

from .resources import Component  # noqa


@extend(Component)
class ExtendComponent(StoreNodePackageConfigs):
    pass


@rule("module", has, "*", fltr_obj=P.fltr_instance(Component))
def module_has_component(module, component):
    module.node_package_configs.add_source(component)
    component.output_path = module.output_path
    component.module = module


@rule(
    "*",
    has,
    "*",
    fltr_subj=P.fltr_instance(Component),
    fltr_obj=P.fltr_instance(Component),
)
def component_has_component(lhs, rhs):
    lhs.node_package_configs.add_source(rhs)
    rhs.module = lhs.module
