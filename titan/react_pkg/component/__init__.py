import moonleap.resource.props as P
from moonleap import (
    Priorities,
    Prop,
    StoreOutputPaths,
    StoreTemplateDirs,
    create,
    create_forward,
    empty_rule,
    extend,
    named,
    rule,
)
from moonleap.parser.term import named_term
from moonleap.verbs import has, wraps
from titan.react_pkg.nodepackage import StoreNodePackageConfigs
from titan.react_pkg.pkg.ml_get import ml_react_app

from . import props
from .resources import Component  # noqa

rules = []


@rule("component", has, "component")
def component_has_component(lhs, rhs):
    return create_forward(lhs, has, named_term(rhs.meta.term))


@rule("component", has, "+component")
def component_has_named_component(lhs, rhs):
    if lhs.module and not rhs.typ.module:
        return create_forward(lhs.module, has, rhs.typ.meta.term)


@rule("component", priority=Priorities.LOW.value)
def create_load_and_select_effects(component):
    if not hasattr(component, "get_chain"):
        return

    effect_relations = props.effect_relations_for_chain(component.get_chain())
    api_module = ml_react_app(component).api_module
    return [
        create_forward(api_module, has, rel.obj, api_module.meta.block)
        for rel in effect_relations
    ] + [
        create_forward(rel.subj, rel.verb, rel.obj, api_module.meta.block)
        for rel in effect_relations
    ]


@create("x+component")
def create_named_component(term, block):
    return named(Component)(term, block)


@extend(Component)
class ExtendComponent(StoreNodePackageConfigs, StoreOutputPaths, StoreTemplateDirs):
    module = P.parent("react-module", has)
    child_components = P.children(has, "+component")


@extend(named(Component))
class ExtendNamedComponent:
    wrapped_child_components = P.children(wraps, "+component")
    # Note that this property returns true if the component or any (grand)child
    # has non-empty component.wrapped_child_components
    wrapped_components = Prop(props.wrapped_components)
