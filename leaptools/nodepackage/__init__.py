import moonleap.resource.props as P
from leapproject.service import Service
from moonleap import MemFun, StoreOutputPaths, extend, render_templates, rule, tags
from moonleap.verbs import has

from . import node_package_configs as NPC
from . import props
from .resources import NodePackage, NodePackageConfig


@tags(["node-package"])
def create_node_package(term, block):
    node_package = NodePackage()
    node_package.node_package_configs.add(
        NodePackageConfig(lambda x: NPC.get(node_package))
    )
    return node_package


@rule("service", has, "node-package")
def service_has_node_package(service, node_package):
    node_package.output_paths.add_source(service)


class StoreNodePackageConfigs:
    node_package_configs = P.tree("has", "node-package-config")


@extend(NodePackage)
class ExtendNodePackage(StoreNodePackageConfigs, StoreOutputPaths):
    render = render_templates(__file__)
    get_config = MemFun(props.get_node_package_config)
    service = P.parent(Service, "has", "node-package")
