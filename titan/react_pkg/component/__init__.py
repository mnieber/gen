import moonleap.packages.extensions.props as P
from moonleap import Prop, create_forward, empty_rule, extend, rule
from moonleap.blocks.verbs import has
from moonleap.packages.rule import Priorities
from titan.react_pkg.reactmodule import ReactModule
from titan.react_view_pkg.widgetregistry import get_widget_reg
from titan.react_view_pkg.widgetregistry.resources import WidgetRegistry
from titan.widgetspec.widget_spec import WidgetSpec

from . import props
from .resources import Component  # noqa

rules = {
    ("widget-registry", has, "component"): empty_rule(),
}


@rule("module", has, "component", priority=Priorities.LOW.value)
def build_component_widget_spec(module, component):
    # Note that this rule has low priority so that it runs after
    # all the component information - which is used in the build function -
    # has been collected.
    return props.build_component_widget_spec(component)


@rule("component")
def created_component(component):
    return create_forward(get_widget_reg(), has, component)


@rule("module", has, "component")
def add_component_widget_spec(module, component):
    term = component.meta.term
    widget_name = term.data + ":" + term.tag

    widget_reg = get_widget_reg()
    if not widget_reg.has(widget_name):
        widget_spec = WidgetSpec()
        widget_spec.widget_name = widget_name
        widget_spec.module_name = module.name
        # We need to add a widget_base_type so that widget_spec.is_component_def
        # returns True.
        widget_spec.widget_base_types = ["Empty"]
        widget_reg.setdefault(widget_spec.widget_name, widget_spec)


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
    widget_spec = Prop(props.component_widget_spec)


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")


@extend(WidgetRegistry)
class ExtendWidgetReg:
    components = P.children(has, "component")
