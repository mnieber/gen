import moonleap.resource.props as P
from moonleap import Prop, create, create_forward, extend, named, rule
from moonleap.parser.term import named_term
from moonleap.verbs import has, wraps
from titan.react_pkg.reactmodule import ReactModule

from . import props
from .resources import Component  # noqa


@rule("module", has, "component")
def module_has_component(module, component):
    module.renders(
        [component],
        "",
        dict(component=component),
        [component.template_dir],
    )


@rule("component", has, "component")
def component_has_component(lhs, rhs):
    return create_forward(lhs, has, named_term(rhs.meta.term))


@rule("component", has, "x+component")
def component_has_named_component(lhs, rhs):
    # TODO: this behaviour is too complex
    if lhs.module and not rhs.typ.module:
        return create_forward(lhs.module, has, rhs.typ.meta.term)


@create("x+generic:component")
def create_named_component(term):
    return named(Component)()


@extend(Component)
class ExtendComponent:
    module = P.parent("react-module", has)
    child_components = P.children(has, "x+component")


@extend(named(Component))
class ExtendNamedComponent:
    wrapped_child_components = P.children(wraps, "x+component")
    # Note that this property returns true if the component or any (grand)child
    # has non-empty component.wrapped_child_components
    wrapped_components = Prop(props.wrapped_components)


@extend(ReactModule)
class ExtendReactModule:
    components = P.children(has, "component")
