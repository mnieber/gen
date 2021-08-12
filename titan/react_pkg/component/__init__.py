import moonleap.resource.props as P
from moonleap import Prop, StoreOutputPaths, create_forward, extend, rule
from moonleap.verbs import has, wraps
from titan.react_pkg.module import Module
from titan.react_pkg.nodepackage import StoreNodePackageConfigs

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
    forwards = [create_forward(lhs, "p-has", ":component", obj_res=rhs)]
    if not rhs.module:
        forwards.append(create_forward(lhs.module, has, ":component", obj_res=rhs))
    return forwards


@rule(
    "*",
    wraps,
    "*",
    fltr_subj=P.fltr_instance(Component),
    fltr_obj=P.fltr_instance(Component),
)
def component_wraps_component(lhs, rhs):
    return create_forward(lhs, "p-wraps", ":component", obj_res=rhs)


@extend(Component)
class ExtendComponent(StoreNodePackageConfigs, StoreOutputPaths):
    wrapped_child_components = P.children("p-wraps", "component")
    child_components = P.children("p-has", "component")
    module = P.parent(Module, has)
    module_path = Prop(props.module_path)
