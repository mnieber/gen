from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, create, extend
from moonleap.verbs import has
from titan.project_pkg.service import Service

from . import props
from .resources import NodePackage  # noqa

base_tags = [("node-package", ["tool"])]


@create("node-package")
def create_node_package(term):
    node_package = NodePackage(name="node-package")
    node_package.template_dir = Path(__file__).parent / "templates"
    node_package.template_context = dict(node_package=node_package)
    return node_package


@extend(NodePackage)
class ExtendNodePackage:
    get_config = MemFun(props.get_node_package_config)


@extend(Service)
class ExtendService:
    node_package = P.child(has, "node-package")
