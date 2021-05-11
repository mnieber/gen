import moonleap.resource.props as P
from moonleap import add, create_forward, extend, rule
from moonleap.verbs import has, uses
from moonleap_project.dockercompose import StoreDockerComposeConfigs
from moonleap_project.service import Service

from . import docker_compose_configs


@rule("service")
def service_created(service):
    if service.use_default_config:
        add(service, docker_compose_configs.get(service, is_dev=True))
        add(service, docker_compose_configs.get(service, is_dev=False))


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    return create_forward(dockerfile.service, has, docker_image)


@rule("service", uses, "service")
def strapi_service_uses_postgres(client_service, server_service):
    add(
        client_service,
        docker_compose_configs.add_depends_on(server_service, is_dev=True),
    )
    add(
        client_service,
        docker_compose_configs.add_depends_on(server_service, is_dev=False),
    )


@extend(Service)
class ExtendService(
    StoreDockerComposeConfigs,
):
    dockerfile = P.child(has, ":dockerfile")
    dockerfile_dev = P.child(has, "dev:dockerfile")
    docker_image = P.child(has, "docker-image")
