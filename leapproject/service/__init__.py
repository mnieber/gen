import moonleap.resource.props as P
from leapdodo.layer import StoreLayerConfigs
from leapproject.dockercompose import StoreDockerComposeConfigs
from leapproject.project import Project
from moonleap import StoreOutputPaths, extend, rule, tags
from moonleap.verbs import configured, has

from . import docker_compose_configs, layer_configs
from .resources import Service


@tags(["service"])
def create_service(term, block):
    service = Service(name=term.data)
    service.output_path = service.name + "/"
    service.layer_configs.add(layer_configs.get_service_options())
    service.docker_compose_configs.add(docker_compose_configs.get(service, is_dev=True))
    service.docker_compose_configs.add(
        docker_compose_configs.get(service, is_dev=False)
    )

    return service


@rule(
    "service",
    has,
    "dockerfile",
    description="""
If the service has a dockerfile then we add docker options to that service.""",
)
def service_has_dockerfile(service, dockerfile):
    service.layer_configs.add(layer_configs.get_docker_options(service))
    dockerfile.output_paths.add_source(service)


@rule("service", configured, "layer")
def service_is_configured_in_layer(service, layer):
    layer.layer_configs.add_source(service)


@extend(Service)
class ExtendService(
    StoreLayerConfigs,
    StoreDockerComposeConfigs,
    StoreOutputPaths,
):
    dockerfile = P.child(has, ":dockerfile")
    dockerfile_dev = P.child(has, "dev:dockerfile")
    layer = P.child(configured, "layer")
    project = P.parent(Project, has, "service")
    src_dir = P.child(has, "src-dir")
