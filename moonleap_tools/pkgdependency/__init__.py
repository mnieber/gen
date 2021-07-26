import typing as T
from dataclasses import dataclass

import moonleap.resource.props as P
from moonleap import MemFun, Resource, extend, register_add
from moonleap.verbs import has
from moonleap_project.service import Service, Tool

from . import props


@dataclass
class PkgDependency(Resource):
    package_names: T.List[str]
    is_dev: bool = False


@register_add(PkgDependency)
def add_pkg_dependency(resource, pkg_dependency):
    resource.pkg_dependencies.add(pkg_dependency)


@extend(Service)
class ExtendService:
    get_pkg_names = MemFun(props.get_pkg_names())


@extend(Tool)
class ExtendTool:
    pkg_dependencies = P.tree(has, "pkg-dependency")
