from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, create, create_forward, empty_rule, extend, rule
from moonleap.verbs import has
from titan.project_pkg.service import Service

from . import props
from .resources import NodePackage, Pkg  # noqa

base_tags = {"node-package": ["tool"]}


rules = {
    ("node-package", has, "node-pkg"): empty_rule(),
}


@create("node-package")
def create_node_package(term):
    node_package = NodePackage(name="node-package")
    node_package.template_dir = Path(__file__).parent / "templates"
    node_package.template_context = dict(node_package=node_package)
    return node_package


@create("node-pkg")
def create_package(term):
    return Pkg(name=term.data)


@rule("cypress")
def created_cypress(cypress):
    return create_forward(":node-package", has, "cypress:node-pkg")


@extend(NodePackage)
class ExtendNodePackage:
    pkgs = P.children(has, "node-pkg")
    has_pkg = MemFun(props.has_pkg)


@extend(Service)
class ExtendService:
    node_package = P.child(has, "node-package")
