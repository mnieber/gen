from titan.react_pkg.reactmodule import ReactModule
from titan.react_view_pkg.pkg.build import build
from titan.react_view_pkg.widgetregistry import get_widget_reg
from titan.react_view_pkg.widgetregistry.resources import WidgetRegistry
from widgetspec.widget_spec import WidgetSpec

import moonleap.packages.extensions.props as P
from moonleap import (
    MemFun,
    Prop,
    create_forward,
    empty_rule,
    extend,
    get_root_resource,
    rule,
)
from moonleap.blocks.verbs import _has_default_prop, _has_prop, has
from moonleap.packages.rule import Priorities

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


@rule("module", has, "component", priority=Priorities.LOW.value)
def build_component_widget_spec(module, component):
    # Note that this rule has low priority so that it runs after
    # all the component information - which is used in the build function -
    # has been collected.
    component.build_output = build(component.widget_spec)
    get_root_resource().set_flags(component.build_output.flags)


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
    pipelines = P.children(has, "x+pipeline")
    get_data_path = MemFun(props.component_get_data_path)
    maybe_expression = MemFun(props.component_maybe_expression)
    named_props = P.children(_has_prop, "x+react-prop")
    named_default_props = P.children(_has_default_prop, "x+react-prop")
    queries = Prop(props.component_queries)
    mutations = Prop(props.component_mutations)


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")


@extend(WidgetRegistry)
class ExtendWidgetReg:
    components = P.children(has, "component")
