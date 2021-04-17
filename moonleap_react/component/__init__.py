from moonleap import extend, rule
from moonleap.verbs import has

from .resources import Component  # noqa


@extend(Component)
class ExtendComponent:
    pass


@rule("module", has, "*", fltr_obj=P.fltr_instance(Component))
def module_has_component(module, component):
    component.module = module


@rule(
    "*",
    has,
    "*",
    fltr_subj=P.fltr_instance(Component),
    fltr_obj=P.fltr_instance(Component),
)
def component_has_component(lhs, rhs):
    rhs.module = lhs.module
