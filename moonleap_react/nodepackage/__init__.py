import moonleap.resource.props as P
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
from moonleap_project.service import Tool

from . import node_package_configs, props
from .resources import NodePackage, NodePackageConfig, load_node_package_config  # noqa


class StoreNodePackageConfigs:
    node_package_configs = P.tree(has, "node-package-config")


@register_add(NodePackageConfig)
def add_node_package_config(resource, node_package_config):
    resource.node_package_configs.add(node_package_config)


@tags(["node-package"])
def create_node_package(term, block):
    node_package = NodePackage()
    add(node_package, node_package_configs.get(node_package))
    return node_package


@rule("service", has, "node-package")
def service_has_node_package(service, node_package):
    node_package.output_paths.add_source(service)


def meta():
    from moonleap_project.service import Service

    @extend(NodePackage)
    class ExtendNodePackage(StoreNodePackageConfigs, StoreOutputPaths):
        render = MemFun(render_templates(__file__))
        get_config = MemFun(props.get_node_package_config)
        service = P.parent(Service, has)

    @extend(Tool)
    class ExtendTool(StoreNodePackageConfigs):
        pass

    return [ExtendNodePackage, ExtendTool]
