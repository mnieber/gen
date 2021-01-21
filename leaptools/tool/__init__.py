import moonleap.resource.props as P
from leapdodo.layer import StoreLayerConfigs
from leapproject.dockercompose import StoreDockerComposeConfigs
from leapproject.service import Service
from leaptools.nodepackage import StoreNodePackageConfigs
from leaptools.optdir import StoreOptPaths
from leaptools.setupfile import StoreSetupFileConfigs
from moonleap import MemFun, Prop, StoreOutputPaths, extend, rule
from moonleap.verbs import has

from . import props
from .resources import Tool


class StoreDependencies:
    pip_dependencies = P.tree("has", "pip-dependency")
    pkg_dependencies = P.tree("has", "pkg-dependency")


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    dockerfile.service.add_tool(docker_image)


class ToolExtensions(
    StoreDependencies,
    StoreDockerComposeConfigs,
    StoreLayerConfigs,
    StoreNodePackageConfigs,
    StoreOptPaths,
    StoreOutputPaths,
    StoreSetupFileConfigs,
):
    pass


def meta():
    from leapproject.dockerfile import DockerImage

    @extend(Tool)
    class ExtendTool(ToolExtensions):
        makefile_rules = P.children("has", "makefile-rule")

    @extend(Service)
    class ExtendService:
        get_pip_pkg_names = MemFun(props.get_pip_pkg_names())
        get_pkg_names = MemFun(props.get_pkg_names())
        makefile_rules = Prop(props.get_makefile_rules())
        opt_dir = P.child(has, "opt-dir")
        tools = P.children(has, "tool")
        add_tool = MemFun(props.add_tool)

    @extend(DockerImage)
    class ExtendDockerImage(ToolExtensions):
        pass

    return [ExtendTool, ExtendService, ExtendDockerImage]
