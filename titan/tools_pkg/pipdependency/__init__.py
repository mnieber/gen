import moonleap.resource.props as P
from moonleap import MemFun, create, extend, register_add
from titan.project_pkg.service import Service, Tool

from . import props
from .resources import PipDependency, PipRequirement


@create("pip-dependency")
def create_pip_dependency(term):
    return PipDependency([term.data], target="base")


@create("dev:pip-dependency")
def create_pip_dependency_dev(term):
    return PipDependency([term.data], target="dev")


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
    pip_dependencies = P.tree("pip_dependencies")
    pip_requirements = P.tree("pip_requirements")
