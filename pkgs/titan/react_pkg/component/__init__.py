from titan.react_pkg.reactmodule import ReactModule
from titan.react_view_pkg.widgetregistry import get_widget_reg
from titan.react_view_pkg.widgetregistry.resources import WidgetRegistry
from widgetspec.widget_spec import WidgetSpec

import moonleap.packages.extensions.props as P
from moonleap import MemFun, create_forward, empty_rule, extend, get_root_resource, rule
from moonleap.blocks.verbs import _has_default_prop, _has_prop, has
from moonleap.packages.rule import Priorities
from pkgs.titan.react_view_pkg.pkg.build import build

from . import props
from .pipelines import (
    create_forwards_for_component_pipelines,
    create_forwards_for_component_props,
)
from .resources import Component  # noqa

rules = {
    ("widget-registry", has, "component"): empty_rule(),
    ("component", has, "x+pipeline"): empty_rule(),
    ("component", _has_prop, "x+react-prop"): empty_rule(),
    ("component", _has_default_prop, "x+react-prop"): empty_rule(),
}


@rule("component")
def add_component_to_widget_reg(component):
    return create_forward(get_widget_reg(), has, component)


@rule("component")
def set_component_pipelines(component):
    return create_forwards_for_component_pipelines(component)


@rule("component")
def set_component_props(component):
    return create_forwards_for_component_props(component)


@rule("component", priority=Priorities.LOW.value)
def build_component_widget_spec(component):
    # Note that this rule has low priority so that it runs after
    # all the component information - which is used in the build function -
    # has been collected.

    widget_reg = get_widget_reg()

    term = component.meta.term
    widget_name = term.data + ":" + term.tag

    # If the widget was defined in the widget-spec yaml file, then widget_name
    # is already known. Otherwise, create the widget-spec.
    widget_spec = widget_reg.get(widget_name, None)
    if not widget_spec:
        widget_spec = WidgetSpec()
        widget_spec.widget_name = widget_name
        # We need to add a widget_base_type so that widget_spec.is_component_def
        # returns True.
        widget_spec.widget_base_types = ["Empty"]
        widget_reg.setdefault(widget_spec.widget_name, widget_spec)

    # Build the widget-spec
    component.build_output = build(widget_spec)
    get_root_resource().set_flags(component.build_output.flags)


@rule("module", has, "component")
def module_has_component(module, component):
    if not component.widget_spec:
        return "retry"

    # Add component to module
    component.widget_spec.module_name = module.name

    # Schedule rendering
    module.renders(
        [component],
        "",
        dict(component=component),
        [component.template_dir],
    )


@extend(Component)
class ExtendComponent:
    module = P.parent("react-module", has)
    pipelines = P.children(has, "x+pipeline")
    get_data_path = MemFun(props.component_get_data_path)
    maybe_expression = MemFun(props.component_maybe_expression)
    named_props = P.children(_has_prop, "x+react-prop")
    named_default_props = P.children(_has_default_prop, "x+react-prop")


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")


@extend(WidgetRegistry)
class ExtendWidgetReg:
    components = P.children(has, "component")
