import moonleap.resource.props as P
from moonleap import MemFun, Prop, create_forward, extend, rule
from moonleap.verbs import provides
from titan.react_pkg.nodepackage import StoreNodePackageConfigs

from . import props
from .resources import Behavior


@rule("state", provides, "*", fltr_obj=P.fltr_instance(Behavior))
def state_provides_a_behavior(state, behavior):
    return create_forward(state, provides, ":behavior", obj_res=behavior)


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    p_section_imports = Prop(props.p_section_imports)
    p_section_constructor = Prop(props.p_section_constructor)
    p_section_callbacks = MemFun(props.p_section_callbacks)
    p_section_declare_policies = MemFun(props.p_section_declare_policies)
    p_section_policies = MemFun(props.p_section_policies)
    p_section_default_props = MemFun(props.p_section_default_props)
