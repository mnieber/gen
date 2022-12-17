import moonleap.resource.props as P
from moonleap import MemFun, create_forward, empty_rule, extend, rule
from moonleap.verbs import has, has_default_prop, has_prop
from titan.react_pkg.reactmodule import ReactModule
from titan.widgets_pkg.widgetregistry import get_widget_reg
from titan.widgets_pkg.widgetregistry.resources import WidgetRegistry

from . import props
from .pipelines import get_pipeline_forwards, get_props_forwards
from .resources import Component  # noqa

rules = {
    ("widget-registry", has, "component"): empty_rule(),
    ("component", has, "x+pipeline"): empty_rule(),
    ("component", has_prop, "click:handler"): empty_rule(),
    ("component", has_prop, "x+pipeline-elm"): empty_rule(),
    ("component", has_default_prop, "x+pipeline-elm"): empty_rule(),
}


@rule("module", has, "component")
def module_has_component(module, component):
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
    return create_forward(get_widget_reg(), has, component)


@extend(Component)
class ExtendComponent:
    module = P.parent("react-module", has)
    pipelines = P.children(has, "x+pipeline")
    get_data_path = MemFun(props.component_get_data_path)
    maybe_expression = MemFun(props.component_maybe_expression)
    named_props = P.children(has_prop, "x+pipeline-elm")
    named_default_props = P.children(has_default_prop, "x+pipeline-elm")


@rule("widget-registry", has, "component")
def component_builder(widget_reg, component):
    props.load_component(component)


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")


@extend(WidgetRegistry)
class ExtendWidgetReg:
    components = P.children(has, "component")
