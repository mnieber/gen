import moonleap.resource.props as P
from moonleap import StoreOutputPaths, add, extend, rule, tags
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import configured, has, uses
from moonleap_dodo.layer import StoreLayerConfigs
from moonleap_project.dockercompose import StoreDockerComposeConfigs
from moonleap_project.project import Project

from . import docker_compose_configs, layer_configs
from .resources import Service


@tags(["service"])
def create_service(term, block):
    service = Service(name=term.data)
    service.output_path = service.name + "/"

    add(service, layer_configs.get_service_options(service))
    add(service, docker_compose_configs.get(service, is_dev=True))
    add(service, docker_compose_configs.get(service, is_dev=False))

    return service


@rule(
    "service",
    has,
    "dockerfile",
    description="""
If the service has a dockerfile then we add docker options to that service.""",
)
def service_has_dockerfile(service, dockerfile):
    add(service, layer_configs.get_docker_options(service))
    dockerfile.output_paths.add_source(service)
    service.docker_compose_configs.add_source(dockerfile)


@rule("service", configured, "layer")
def service_is_configured_in_layer(service, layer):
    layer.layer_configs.add_source(service)


@rule("service", uses, "port")
def service_uses_port(service, port):
    service.port = port.term.data


@extend(Service)
class ExtendService(
    StoreLayerConfigs,
    StoreDockerComposeConfigs,
    StoreOutputPaths,
    StoreTemplateDirs,
):
    dockerfile = P.child(has, ":dockerfile")
    dockerfile_dev = P.child(has, "dev:dockerfile")
    layer = P.child(configured, "layer")
    project = P.parent(Project, has, "service")
    src_dir = P.child(has, "src-dir")
