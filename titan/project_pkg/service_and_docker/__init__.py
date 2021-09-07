import moonleap.resource.props as P
from moonleap import add, create_forward, empty_rule, extend, rule
from moonleap.verbs import has, uses
from titan.project_pkg.dockercompose import StoreDockerComposeConfigs
from titan.project_pkg.service import Service

from . import docker_compose_configs


@rule("service")
def service_created(service):
    if service.use_default_config:
        add(service, docker_compose_configs.get(service, is_dev=True))
        add(service, docker_compose_configs.get(service, is_dev=False))


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    return create_forward(dockerfile.service, has, docker_image._meta.term)


@rule("service", uses, "service")
def service_uses_service(client_service, server_service):
    for is_dev in (True, False):
        add(
            client_service,
            docker_compose_configs.add_depends_on(server_service, is_dev=is_dev),
        )


rules = [(("service", has, "docker-image"), empty_rule())]


@extend(Service)
class ExtendService(
    StoreDockerComposeConfigs,
):
    dockerfile = P.child(has, "dockerfile")
    docker_image = P.child(has, "docker-image")
