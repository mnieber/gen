import moonleap.resource.props as P
from moonleap import (
    StoreOutputPaths,
    StoreTemplateDirs,
    create_forward,
    empty_rule,
    extend,
    rule,
)
from moonleap.verbs import has, wraps
from titan.react_pkg.module import Module
from titan.react_pkg.nodepackage import StoreNodePackageConfigs

from .resources import Component  # noqa

rules = [
    (("component", wraps, "component"), empty_rule()),
    (("component", has, "component"), empty_rule()),
]


@rule("component", has, "component")
def component_has_component(lhs, rhs):
    if lhs.module and not rhs.module:
        return create_forward(lhs.module, has, rhs._meta.term)


@extend(Component)
class ExtendComponent(StoreNodePackageConfigs, StoreOutputPaths, StoreTemplateDirs):
    wrapped_child_components = P.children(wraps, "component")
    child_components = P.children(has, "component")
    module = P.parent(Module, has)
