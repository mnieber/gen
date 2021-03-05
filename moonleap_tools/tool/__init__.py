import moonleap.resource.props as P
from moonleap import MemFun, Prop, StoreOutputPaths, extend, rule
from moonleap.verbs import has
from moonleap_dodo.layer import StoreLayerConfigs
from moonleap_project.dockercompose import StoreDockerComposeConfigs
from moonleap_project.service import Service, service_has_tool_rel
from moonleap_tools.optdir import StoreOptPaths
from moonleap_tools.setupfile import StoreSetupFileConfigs

from . import props
from .resources import Tool


class StoreDependencies:
    pip_dependencies = P.tree("has", "pip-dependency")
    pip_requirements = P.tree("has", "pip-requirement")
    pkg_dependencies = P.tree("has", "pkg-dependency")


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    return service_has_tool_rel(dockerfile.service, docker_image)


@rule("service", has, "tool")
def service_has_tool(service, tool):
    tool.output_paths.add_source(service)


# We define this here instead of in the makefile package to work
# around python circular import problems
class StoreMakefileRules:
    makefile_rules = P.tree(has, "makefile")


class ToolExtensions(
    StoreDependencies,
    StoreDockerComposeConfigs,
    StoreLayerConfigs,
    StoreMakefileRules,
    StoreOptPaths,
    StoreOutputPaths,
    StoreSetupFileConfigs,
):
    pass


def meta():
    from moonleap_project.dockerfile import DockerImage

    @extend(Tool)
    class ExtendTool(ToolExtensions):
        pass

    @extend(Service)
    class ExtendService:
        get_pip_pkg_names = MemFun(props.get_pip_pkg_names())
        get_pip_requirements = MemFun(props.get_pip_requirements())
        get_pkg_names = MemFun(props.get_pkg_names())
        makefile_rules = Prop(props.get_makefile_rules())
        opt_dir = P.child(has, "opt-dir")
        tools = P.children(has, "tool")

    @extend(DockerImage)
    class ExtendDockerImage(ToolExtensions):
        pass

    return [ExtendTool, ExtendService, ExtendDockerImage]
