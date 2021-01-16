import moonleap.resource.props as P
from leap_mn.dockercompose import DockerComposeConfig, StoreDockerComposeConfigs
from leap_mn.project import Project
from leapdodo.layer import LayerConfig, StoreLayerConfigs
from moonleap import MemFun, Prop, StoreOutputPaths, extend, rule, tags

from . import docker_compose_configs as DCC
from . import layer_configs as LC
from . import props
from .resources import Service


@tags(["service"])
def create_service(term, block):
    service = Service(name=term.data)
    service.output_path = service.name + "/"
    service.layer_configs.add(LayerConfig(body=LC.get_service_options()))
    service.docker_compose_configs.add(
        DockerComposeConfig(
            lambda docker_compose_config: DCC.get_service_options(
                service, docker_compose_config
            )
        )
    )
    service.docker_compose_configs.add(
        DockerComposeConfig(
            lambda docker_compose_config: DCC.get_service_options(
                service, docker_compose_config
            ),
            is_dev=True,
        )
    )
    return service


@rule(
    "service",
    "has",
    "dockerfile",
    description="""
If the service has a dockerfile then we add docker options to that service.""",
)
def service_has_dockerfile(service, dockerfile):
    service.layer_configs.add(LayerConfig(lambda: LC.get_docker_options(service)))
    dockerfile.output_paths.add_source(service)


@rule("service", "configured", "layer")
def service_is_configured_in_layer(service, layer):
    layer.layer_configs.add_source(service)


@extend(Service)
class ExtendService(StoreLayerConfigs, StoreDockerComposeConfigs, StoreOutputPaths):
    dockerfile = P.child("has", ":dockerfile")
    dockerfile_dev = P.child("has", "dev:dockerfile")
    get_pip_pkg_names = MemFun(props.get_pip_pkg_names())
    get_pkg_names = MemFun(props.get_pkg_names())
    layer = P.child("configured", "layer")
    makefile_rules = Prop(props.get_makefile_rules())
    project = P.parent(Project, "has", "service")
    src_dir = P.child("has", "src-dir")
    tools = P.children(("has", "uses"), "tool")
