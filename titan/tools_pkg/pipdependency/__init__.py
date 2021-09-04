import moonleap.resource.props as P
from moonleap import MemFun, extend, register_add, tags
from titan.project_pkg.service import Service, Tool

from . import props
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


@extend(Service)
class ExtendService:
    get_pip_pkg_names = MemFun(props.get_pip_pkg_names())
    get_pip_requirements = MemFun(props.get_pip_requirements())


@extend(Tool)
class ExtendTool:
    pip_dependencies = P.tree("p-has", "pip-dependency")
    pip_requirements = P.tree("p-has", "pip-requirement")
