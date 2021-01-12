from dataclasses import dataclass

from moonleap import Resource


@dataclass
class PkgDependency(Resource):
    package_names: [str]
    is_dev: bool = False


def meta():
    return []
