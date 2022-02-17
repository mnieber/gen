from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    StoreOutputPaths,
    add,
    create,
    extend,
    feeds,
    receives,
    register_add,
)
from moonleap.verbs import has, runs
from titan.project_pkg.service import Service, Tool

from . import node_package_configs, props
from .resources import NodePackage, NodePackageConfig, load_node_package_config  # noqa

rules = [
    (("service", has, "node-package"), feeds("node_package_configs")),
    (("service", has + runs, "tool"), receives("node_package_configs")),
    (("react-app", has, "module"), receives("node_package_configs")),
]

base_tags = [("node-package", ["tool"])]


class StoreNodePackageConfigs:
    node_package_configs = P.tree("node_package_configs")


@register_add(NodePackageConfig)
def add_node_package_config(resource, node_package_config):
    resource.node_package_configs.add(node_package_config)


@create("node-package")
def create_node_package(term):
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
