import typing as T
from dataclasses import dataclass

from moonleap import Resource, register_add


@dataclass
class PkgDependency(Resource):
    package_names: T.List[str]
    is_dev: bool = False


@register_add(PkgDependency)
def add_pkg_dependency(resource, pkg_dependency):
    resource.pkg_dependencies.add(pkg_dependency)
