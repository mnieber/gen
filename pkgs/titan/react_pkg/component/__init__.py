from titan.react_pkg.reactmodule import ReactModule
from titan.react_view_pkg.widgetregistry import get_widget_reg
from titan.react_view_pkg.widgetregistry.resources import WidgetRegistry
from widgetspec.widget_spec import WidgetSpec

import moonleap.packages.extensions.props as P
from moonleap import MemFun, create_forward, empty_rule, extend, rule
from moonleap.blocks.verbs import _has_default_prop, _has_prop, has

from . import props
from .pipelines import get_pipeline_forwards, get_props_forwards
from .resources import Component  # noqa

rules = {
    ("widget-registry", has, "component"): empty_rule(),
    ("component", has, "x+pipeline"): empty_rule(),
    ("component", _has_prop, "x+react-prop"): empty_rule(),
    ("component", _has_default_prop, "x+react-prop"): empty_rule(),
}


@rule("module", has, "component")
def module_has_component(module, component):
    term = component.meta.term
    widget_name = term.data + ":" + term.tag

    # If the widget was defined in the widget-spec yaml file, then widget_name
    # is already known. Otherwise, create the widget-spec.
    if not get_widget_reg().has(widget_name):
        widget_spec = WidgetSpec()
        widget_spec.widget_name = widget_name
        widget_spec.module_name = module.name
        get_widget_reg().setdefault(widget_spec.widget_name, widget_spec)

    module.renders(
        [component],
        "",
        dict(component=component),
        [component.template_dir],
    )


@rule("component")
def set_component_pipelines(component):
    return get_pipeline_forwards(component)


@rule("component")
def set_component_props(component):
    return get_props_forwards(component)


@rule("component")
def created_component(component):
    from titan.react_view_pkg.widgetregistry import get_widget_reg

    return create_forward(get_widget_reg(), has, component)


@extend(Component)
class ExtendComponent:
    module = P.parent("react-module", has)
    pipelines = P.children(has, "x+pipeline")
    get_data_path = MemFun(props.component_get_data_path)
    maybe_expression = MemFun(props.component_maybe_expression)
    named_props = P.children(_has_prop, "x+react-prop")
    named_default_props = P.children(_has_default_prop, "x+react-prop")


@rule("widget-registry", has, "component")
def component_builder(widget_reg, component):
    props.load_component(component)


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")


@extend(WidgetRegistry)
class ExtendWidgetReg:
    components = P.children(has, "component")
