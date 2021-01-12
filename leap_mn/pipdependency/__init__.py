from moonleap import tags

from .resources import PipDependency


@tags(["pip-dependency"])
def create_pip_dependency(term, block):
    return PipDependency([term.data])


@tags(["dev:pip-dependency"])
def create_pip_dependency_dev(term, block):
    return PipDependency([term.data], is_dev=True)


def meta():
    return []
