import moonleap.resource.props as P
from moonleap import add, extend, rule, tags
from moonleap.verbs import has
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config
from moonleap_react.nodepackage.__init__ import StoreNodePackageConfigs
from moonleap_tools.tool import Tool

from .resources import Behavior


@tags(["behavior"])
def create_behavior(term, block):
    behavior = Behavior(name=term.data)
    add(behavior, load_node_package_config(__file__))
    return behavior


@rule("module", has, "behavior")
def module_has_behavior(module, behavior):
    module.node_package_configs.add_source(behavior)


@extend(Module)
class ExtendModule:
    behaviors = P.children("has", "behavior")


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    pass
