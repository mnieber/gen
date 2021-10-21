import moonleap.resource.props as P
from moonleap import create_forward, empty_rule, extend, feeds, receives, rule
from moonleap.verbs import has, shows
from titan.react_pkg.module import Module

rules = [
    (("module", has, "component"), receives("node_package_configs")),
    (("module", has, "component"), receives("react_app_configs")),
    (("module", has, "component"), feeds("output_paths")),
    (("module", shows, "+component"), empty_rule()),
]


@extend(Module)
class ExtendModule:
    routed_components = P.children(shows, "+component")
