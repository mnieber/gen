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
from moonleap.verbs import has, has_default_prop, has_prop
from titan.react_pkg.reactmodule import ReactModule
from titan.widgets_pkg.widgetregistry import get_widget_reg
from titan.widgets_pkg.widgetregistry.resources import WidgetRegistry

from . import props
from .pipelines import component_load_pipelines
from .resources import Component  # noqa

rules = {
    ("widget-registry", has, "component"): empty_rule(),
    ("component", has, "x+pipeline"): empty_rule(),
    ("component", has_prop, "x+pipeline-elm"): empty_rule(),
    ("component", has_default_prop, "x+pipeline-elm"): empty_rule(),
    ("component", has_default_prop, "behavior"): empty_rule(),
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
    load_pipelines = MemFun(component_load_pipelines)
    pipelines = P.children(has, "x+pipeline")
    get_pipeline_and_data_path = MemFun(props.component_get_pipeline_and_data_path)
    maybe_expression = MemFun(props.component_maybe_expression)
    named_props = P.children(has_prop, "x+pipeline-elm")
    named_default_props = P.children(has_default_prop, "x+pipeline-elm")
    bvr_default_props = P.children(has_default_prop, "behavior")


@rule("widget-registry", has, "component", priority=Priorities.LOW.value)
def component_builder(widget_reg, component):
    from titan.react_view_pkg.pkg.get_builder import get_builder

    if widget_spec := component.widget_spec:
        builder = get_builder(widget_spec, parent_builder=None)
        component.builder = builder
        builder.build()
        forwards = []

        for default_prop in builder.output.default_props:
            forwards.append(create_forward(component, has_default_prop, default_prop))

        return forwards


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")


@extend(WidgetRegistry)
class ExtendWidgetReg:
    components = P.children(has, "component")
