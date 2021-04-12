import moonleap.resource.props as P
from moonleap import StoreOutputPaths, extend
from moonleap_dodo.layer import StoreLayerConfigs
from moonleap_project.dockercompose import StoreDockerComposeConfigs
from moonleap_react.component import StoreCssImports
from moonleap_react.nodepackage import StoreNodePackageConfigs
from moonleap_tools.makefile import StoreMakefileRules
from moonleap_tools.optdir import StoreOptPaths
from moonleap_tools.setupfile import StoreSetupFileConfigs
from moonleap_tools.tool import Tool


class StoreDependencies:
    pip_dependencies = P.tree("has", "pip-dependency")
    pip_requirements = P.tree("has", "pip-requirement")
    pkg_dependencies = P.tree("has", "pkg-dependency")


class ToolExtensions(
    StoreCssImports,
    StoreDependencies,
    StoreDockerComposeConfigs,
    StoreLayerConfigs,
    StoreMakefileRules,
    StoreNodePackageConfigs,
    StoreOptPaths,
    StoreOutputPaths,
    StoreSetupFileConfigs,
):
    pass


@extend(Tool)
class ExtendTool(ToolExtensions):
    pass
