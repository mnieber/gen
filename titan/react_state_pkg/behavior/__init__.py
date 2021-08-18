import moonleap.resource.props as P
from moonleap import Prop, create_forward, extend, rule
from moonleap.verbs import provides
from titan.react_pkg.nodepackage import StoreNodePackageConfigs

from . import props
from .resources import Behavior


@rule("state", provides, "*", fltr_obj=P.fltr_instance(Behavior))
def state_provides_a_behavior(state, behavior):
    return create_forward(state, provides, ":behavior", obj_res=behavior)


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    sections = Prop(props.Sections)
