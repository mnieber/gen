import moonleap.resource.props as P
from leapdodo.layer import StoreLayerConfigs
from leapproject.dockercompose import StoreDockerComposeConfigs
from leapproject.service import Service
from leaptools.nodepackage import StoreNodePackageConfigs
from leaptools.optdir import StoreOptPaths
from leaptools.setupfile import StoreSetupFileConfigs
from moonleap import MemFun, Prop, StoreOutputPaths, extend, rule

from . import props
from .resources import Tool


class StoreDependencies:
    pip_dependencies = P.tree("has", "pip-dependency")
    pkg_dependencies = P.tree("has", "pkg-dependency")


@rule("service", ("has", "uses"), "*", fltr_obj=P.fltr_instance("leaptools.tool.Tool"))
def service_has_tool(service, tool):
    service.add_to_tools(tool)
    service.layer_configs.add_source(tool)
    service.docker_compose_configs.add_source(tool)
    service.setup_file_configs.add_source(tool)
    tool.output_paths.add_source(service)


@extend(Tool)
class ExtendTool(
    StoreDependencies,
    StoreDockerComposeConfigs,
    StoreLayerConfigs,
    StoreNodePackageConfigs,
    StoreOptPaths,
    StoreOutputPaths,
    StoreSetupFileConfigs,
):
    makefile_rules = P.children("has", "makefile-rule")


@extend(Service)
class ExtendService(
    StoreSetupFileConfigs,
):
    get_pip_pkg_names = MemFun(props.get_pip_pkg_names())
    get_pkg_names = MemFun(props.get_pkg_names())
    makefile_rules = Prop(props.get_makefile_rules())
    opt_dir = P.child("has", "opt-dir")
    tools = P.children(("has", "uses"), "tool")
