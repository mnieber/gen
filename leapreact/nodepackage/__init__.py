import moonleap.resource.props as P
from leapproject.service import Service
from leaptools.tool import Tool
from moonleap import (
    MemFun,
    StoreOutputPaths,
    add,
    extend,
    register_add,
    render_templates,
    rule,
    tags,
)
from moonleap.verbs import has

from . import node_package_configs, props
from .resources import NodePackage, NodePackageConfig  # noqa


@tags(["node-package"])
def create_node_package(term, block):
    node_package = NodePackage()
    add(node_package, node_package_configs.get(node_package))
    return node_package


@rule("service", has, "node-package")
def service_has_node_package(service, node_package):
    node_package.output_paths.add_source(service)


@register_add(NodePackageConfig)
def add_node_package_config(resource, node_package_config):
    resource.node_package_configs.add(node_package_config)


class StoreNodePackageConfigs:
    node_package_configs = P.tree("has", "node-package-config")


@extend(NodePackage)
class ExtendNodePackage(StoreNodePackageConfigs, StoreOutputPaths):
    render = render_templates(__file__)
    get_config = MemFun(props.get_node_package_config)
    service = P.parent(Service, "has", "node-package")


@extend(Tool)
class ExtendTool(StoreNodePackageConfigs):
    pass
