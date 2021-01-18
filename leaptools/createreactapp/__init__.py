from leaptools.nodepackage import (
    NodePackageConfig,
    StoreNodePackageConfigs,
    create_node_package,
)
from leaptools.tool import Tool
from moonleap import extend, rule, tags

from . import node_package_configs as NPC


class CreateReactApp(Tool):
    pass


@tags(["create-react-app"])
def create_cra(term, block):
    cra = CreateReactApp()
    cra.node_package_configs.add(NodePackageConfig(NPC.get()))
    return cra


@rule("node-package", "uses", "create-react-app")
def node_package_uses_cra(node_package, cra):
    node_package.node_package_configs.add_source(cra)
