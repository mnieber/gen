from moonleap import Priorities, register_add, rule, tags
from moonleap.verbs import has

from .resources import PipDependency, PipRequirement


@tags(["pip-dependency"])
def create_pip_dependency(term, block):
    return PipDependency([term.data])


@tags(["dev:pip-dependency"])
def create_pip_dependency_dev(term, block):
    return PipDependency([term.data], is_dev=True)


@register_add(PipDependency)
def add_pip_dependency(resource, pip_dependency):
    resource.pip_dependencies.add(pip_dependency)


@register_add(PipRequirement)
def add_pip_requirement(resource, pip_requirement):
    resource.pip_requirements.add(pip_requirement)
