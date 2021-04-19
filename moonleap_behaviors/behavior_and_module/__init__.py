import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from moonleap_react.module import Module


@rule("module", has, "behavior")
def module_has_behavior(module, behavior):
    module.node_package_configs.add_source(behavior)


@extend(Module)
class ExtendModule:
    behaviors = P.children("has", "behavior")
