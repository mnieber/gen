from moonleap import register_add, tags

from .resources import PipDependency


@tags(["pip-dependency"])
def create_pip_dependency(term, block):
    return PipDependency([term.data])


@tags(["dev:pip-dependency"])
def create_pip_dependency_dev(term, block):
    return PipDependency([term.data], is_dev=True)


@register_add(PipDependency)
def add_pip_dependency(resource, pip_dependency):
    resource.pip_dependencies.add(pip_dependency)
