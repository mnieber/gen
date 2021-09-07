from moonleap import Prop, extend
from titan.react_pkg.nodepackage import StoreNodePackageConfigs

from . import props
from .resources import Behavior


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    sections = Prop(props.Sections)
