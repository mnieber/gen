import moonleap.extension.props as P
from moonleap import empty_rule, extend, rule
from moonleap.spec.verbs import has
from titan.react_pkg.reactmodule import ReactModule

from .resources import Component  # noqa


@extend(Component)
class ExtendComponent:
    module = P.parent("react-module", has)


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")


rules = {
    "widget-registry": {(has, "component"): empty_rule()},
    "module": {(has, "component"): empty_rule()},
}
