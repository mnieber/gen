import moonleap.resource.props as P
from moonleap import Prop, empty_rule, extend, named
from moonleap.verbs import has
from titan.api_pkg.itemlist.resources import ItemList
from titan.react_pkg.nodepackage import StoreNodePackageConfigs

from . import props
from .resources import Behavior

rules = [
    (("x+item~list", has, "behavior"), empty_rule()),
]


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    sections = Prop(props.Sections)


@extend(named(ItemList))
class ExtendNamedItemList:
    bvrs = P.children(has, "behavior")
