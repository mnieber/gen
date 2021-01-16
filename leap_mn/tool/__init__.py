import moonleap.resource.props as P
from leap_mn.dockercompose import StoreDockerComposeConfigs
from leap_mn.optdir import StoreOptPaths
from leapdodo.layer import StoreLayerConfigs
from moonleap import StoreOutputPaths, extend, rule

from .resources import Tool


@rule("service", ("has", "uses"), "*", fltr_obj=P.fltr_instance(Tool))
def service_has_tool(service, tool):
    service.add_to_tools(tool)
    service.layer_configs.add_source(tool)
    service.docker_compose_configs.add_source(tool)
    tool.output_paths.add_source(service)


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
):
    makefile_rules = P.children("has", "makefile-rule")
