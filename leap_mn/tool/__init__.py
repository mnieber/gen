import moonleap.resource.props as P
from leap_mn.dockercompose import StoreDockerComposeConfigs
from leap_mn.optdir import StoreOptPaths
from leap_mn.setupfile import StoreSetupFileConfigs
from leapdodo.layer import StoreLayerConfigs
from moonleap import StoreOutputPaths, extend

from .resources import Tool


class StoreDependencies:
    pip_dependencies = P.tree(
        "has", "pip-dependency", merge=lambda acc, x: [*acc, x], initial=list()
    )
    pkg_dependencies = P.tree(
        "has", "pkg-dependency", merge=lambda acc, x: [*acc, x], initial=list()
    )


@extend(Tool)
class ExtendTool(
    StoreLayerConfigs,
    StoreOptPaths,
    StoreDependencies,
    StoreOutputPaths,
    StoreDockerComposeConfigs,
    StoreSetupFileConfigs,
):
    makefile_rules = P.children("has", "makefile-rule")
