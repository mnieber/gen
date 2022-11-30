import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Priorities,
    create,
    create_forward,
    empty_rule,
    extend,
    named,
    rule,
)
from moonleap.verbs import has
from titan.react_pkg.reactmodule import ReactModule
from titan.widgets_pkg.widgetregistry import get_widget_reg
from titan.widgets_pkg.widgetregistry.resources import WidgetRegistry

from . import props
from .resources import Component  # noqa

rules = {
    ("widget-registry", has, "component"): empty_rule(),
    ("component", has, "x+pipeline"): empty_rule(),
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
    return component.load_pipelines()


@create("x+generic:component")
def create_named_component(term):
    return named(Component)()


@rule("component", priority=Priorities.LOW.value)
def created_component(component):
    return create_forward(get_widget_reg(), has, component)


@extend(Component)
class ExtendComponent:
    module = P.parent("react-module", has)
    load_pipelines = MemFun(props.load_pipelines)
    pipelines = P.children(has, "x+pipeline")
    get_pipeline = MemFun(props.component_get_pipeline)
    get_expression = MemFun(props.component_get_expression)
    maybe_expression = MemFun(props.component_maybe_expression)


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")


@extend(WidgetRegistry)
class ExtendWidgetReg:
    components = P.children(has, "component")
