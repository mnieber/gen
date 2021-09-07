from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    StoreOutputPaths,
    add,
    add_src,
    add_src_inv,
    create,
    extend,
    register_add,
)
from moonleap.verbs import has
from titan.project_pkg.service import Service, Tool

from . import node_package_configs, props
from .resources import NodePackage, NodePackageConfig, load_node_package_config  # noqa

rules = [
    (("service", has, "node-package"), add_src_inv("node_package_configs")),
    (("service", has, "tool"), add_src("node_package_configs")),
    (("react-app", has, "module"), add_src("node_package_configs")),
]


class StoreNodePackageConfigs:
    node_package_configs = P.tree("p-has", "node-package-config")


@register_add(NodePackageConfig)
def add_node_package_config(resource, node_package_config):
    resource.node_package_configs.add(node_package_config)


@create("node-package", ["tool"])
def create_node_package(term, block):
    node_package = NodePackage(name="node-package")
    node_package.add_template_dir(Path(__file__).parent / "templates")
    add(node_package, node_package_configs.get(node_package))
    return node_package


@extend(NodePackage)
class ExtendNodePackage(StoreNodePackageConfigs, StoreOutputPaths):
    get_config = MemFun(props.get_node_package_config)


@extend(Tool)
class ExtendTool(StoreNodePackageConfigs):
    pass


@extend(Service)
class ExtendService(StoreNodePackageConfigs):
    pass
