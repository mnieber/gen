import moonleap.resource.props as P
from moonleap import add, add_source, extend, rule
from moonleap.verbs import has
from moonleap_project.dockercompose import StoreDockerComposeConfigs
from moonleap_project.service import Service, service_has_tool_rel

from . import docker_compose_configs


@rule("service")
def service_created(service):
    if service.use_default_config:
        add(service, docker_compose_configs.get(service, is_dev=True))
        add(service, docker_compose_configs.get(service, is_dev=False))


@rule("service", has, "dockerfile")
def service_has_dockerfile(service, dockerfile):
    dockerfile.output_paths.add_source(service)
    add_source(
        [service, "docker_compose_configs"],
        dockerfile,
        "The :service receives docker compose configs from a :dockerfile",
    )


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    return service_has_tool_rel(dockerfile.service, docker_image)


@extend(Service)
class ExtendService(
    StoreDockerComposeConfigs,
):
    dockerfile = P.child(has, ":dockerfile")
    dockerfile_dev = P.child(has, "dev:dockerfile")
