import moonleap.resource.props as P
from moonleap import Prop, create_forward, extend, rule
from moonleap.verbs import has, supports
from moonleap_react.nodepackage import StoreNodePackageConfigs
from moonleap_react_state.state.resources import State

from . import props
from .resources import Behavior


@rule("state", supports, "*", fltr_obj=P.fltr_instance(Behavior))
def state_supports_a_behavior(state, behavior):
    return create_forward(state, has, ":behavior", obj_res=behavior)


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    state = P.parent(State, has, "behavior")

    imports_section = Prop(props.imports_section)
    constructor_section = Prop(props.constructor_section)
    callbacks_section = Prop(props.callbacks_section)
    declare_policies_section = Prop(props.declare_policies_section)
    policies_section = Prop(props.policies_section)
