import moonleap.resource.props as P
from moonleap import Priorities, create, create_forward, empty_rule, extend, named, rule
from moonleap.verbs import has
from titan.react_pkg.reactmodule import ReactModule
from titan.widgets_pkg.widgetregistry import get_widget_reg
from titan.widgets_pkg.widgetregistry.resources import WidgetRegistry

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


@create("x+generic:component")
def create_named_component(term):
    return named(Component)()


@rule("component", priority=Priorities.LOW.value)
def created_component(component):
    return create_forward(get_widget_reg(), has, component)


@extend(Component)
class ExtendComponent:
    module = P.parent("react-module", has)


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")


@extend(WidgetRegistry)
class ExtendWidgetReg:
    components = P.children(has, "component")
