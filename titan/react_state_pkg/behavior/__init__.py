import moonleap.resource.props as P
from moonleap import Prop, extend
from moonleap.verbs import provides
from titan.react_pkg.nodepackage import StoreNodePackageConfigs
from titan.react_state_pkg.state.resources import State

from . import props
from .resources import Behavior


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    sections = Prop(props.Sections)
    state = P.parent("state", provides)
