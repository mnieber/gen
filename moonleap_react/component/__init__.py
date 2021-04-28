import moonleap.resource.props as P
from moonleap import StoreOutputPaths, create_forward, extend, rule
from moonleap.verbs import has, wraps
from moonleap_react.nodepackage import StoreNodePackageConfigs

from .resources import Component  # noqa


@rule(
    "*",
    has,
    "*",
    fltr_subj=P.fltr_instance(Component),
    fltr_obj=P.fltr_instance(Component),
)
def component_has_component(lhs, rhs):
    lhs.add_to_children(rhs)
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
    lhs.add_to_wrapped_children(rhs)


@extend(Component)
class ExtendComponent(StoreNodePackageConfigs, StoreOutputPaths):
    wrapped_children = P.children(wraps, "component")
    children = P.children(has, "component")
