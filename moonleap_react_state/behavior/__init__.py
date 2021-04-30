import moonleap.resource.props as P
from moonleap import MemFun, Prop, create_forward, extend, rule
from moonleap.verbs import provides
from moonleap_react.nodepackage import StoreNodePackageConfigs

from . import props
from .resources import Behavior


@rule("state", provides, "*", fltr_obj=P.fltr_instance(Behavior))
def state_provides_a_behavior(state, behavior):
    return create_forward(state, provides, ":behavior", obj_res=behavior)


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    item_name = Prop(props.item_name)

    imports_section = Prop(props.imports_section)
    constructor_section = Prop(props.constructor_section)
    callbacks_section = MemFun(props.callbacks_section)
    declare_policies_section = MemFun(props.declare_policies_section)
    policies_section = MemFun(props.policies_section)
