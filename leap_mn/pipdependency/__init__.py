from dataclasses import dataclass

from moonleap import Resource, tags


@dataclass
class PipDependency(Resource):
    package_names: [str]
    is_dev: bool = False


@tags(["pip-dependency"])
def create_pip_dependency(term, block):
    return PipDependency([term.data])


@tags(["dev:pip-dependency"])
def create_pip_dependency_dev(term, block):
    return PipDependency([term.data], is_dev=True)


def meta():
    return []
