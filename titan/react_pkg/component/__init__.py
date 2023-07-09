import moonleap.packages.extensions.props as P
from moonleap import empty_rule, extend, rule
from moonleap.blocks.verbs import has
from titan.react_pkg.reactmodule import ReactModule

from .resources import Component  # noqa

rules = {
    ("widget-registry", has, "component"): empty_rule(),
}


@rule("module", has, "component")
def module_has_component(module, component):
    module.renders(
        [component],
        "",
        dict(component=component),
        [component.template_dir],
    )


@extend(Component)
class ExtendComponent:
    module = P.parent("react-module", has)


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")
