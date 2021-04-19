from moonleap import add, extend, tags
from moonleap_react.nodepackage import StoreNodePackageConfigs, load_node_package_config

from .resources import Behavior


@tags(["behavior"])
def create_behavior(term, block):
    behavior = Behavior(name=term.data)
    add(behavior, load_node_package_config(__file__))
    return behavior


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    pass
