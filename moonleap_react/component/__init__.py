import moonleap.resource.props as P
from moonleap import Prop, StoreOutputPaths, create_forward, extend, rule
from moonleap.verbs import has, wraps
from moonleap_react.module import Module
from moonleap_react.nodepackage import StoreNodePackageConfigs

from . import props
from .resources import Component  # noqa


@rule(
    "*",
    has,
    "*",
    fltr_subj=P.fltr_instance(Component),
    fltr_obj=P.fltr_instance(Component),
)
def component_has_component(lhs, rhs):
    lhs.add_to_child_components(rhs)
    if not rhs.module:
        return create_forward(lhs.module, has, rhs)


@rule(
    "*",
    wraps,
    "*",
    fltr_subj=P.fltr_instance(Component),
    fltr_obj=P.fltr_instance(Component),
)
def component_wraps_component(lhs, rhs):
    lhs.add_to_wrapped_child_components(rhs)


@extend(Component)
class ExtendComponent(StoreNodePackageConfigs, StoreOutputPaths):
    wrapped_child_components = P.children(wraps, "component")
    child_components = P.children(has, "component")
    module = P.parent(Module, has)
    module_path = Prop(props.module_path)
