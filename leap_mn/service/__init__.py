import moonleap.resource.props as P
from leap_mn.dockercompose import DockerComposeConfig, StoreDockerComposeConfigs
from leap_mn.project import Project
from leapdodo.layer import LayerConfig, StoreLayerConfigs
from moonleap import StoreOutputPaths, extend, rule, tags

from . import docker_compose_configs as DCC
from . import layer_configs as LC
from .resources import Service


@tags(["service"])
def create_service(term, block):
    service = Service(name=term.data)
    service.output_path = service.name + "/"
    service.layer_configs.add(LayerConfig(body=LC.get_service_options()))

    def _create_dcc(is_dev):
        return DockerComposeConfig(
            lambda x: DCC.get_service_options(service, is_dev=is_dev), is_dev=is_dev
        )

    for is_dev in (True, False):
        service.docker_compose_configs.add(_create_dcc(is_dev))

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
class ExtendService(
    StoreLayerConfigs,
    StoreDockerComposeConfigs,
    StoreOutputPaths,
):
    dockerfile = P.child("has", ":dockerfile")
    dockerfile_dev = P.child("has", "dev:dockerfile")
    layer = P.child("configured", "layer")
    project = P.parent(Project, "has", "service")
    src_dir = P.child("has", "src-dir")
