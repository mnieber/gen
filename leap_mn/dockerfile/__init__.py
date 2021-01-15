import moonleap.props as P
from leap_mn.layer import LayerConfig
from leap_mn.service import Service
from moonleap import extend, output_dir_from, rule, tags

from . import layer_configs as LC
from .resources import Dockerfile


@tags(["dockerfile"])
def create_dockerfile(term, block):
    docker_file = Dockerfile()
    return docker_file


@tags(["dev:dockerfile"])
def create_dockerfile_dev(term, block):
    return Dockerfile(is_dev=True)


@rule("dockerfile", "use", "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    dockerfile.image_name = docker_image.term.data


@rule(
    "service",
    "has",
    "dockerfile",
    description="""
If the service has a dockerfile then we add docker options to that service.""",
)
def service_has_dockerfile(service, dockerfile):
    if service:
        service.layer_configs.add(
            #
            LayerConfig(lambda: LC.get_docker_options(service))
        )


@extend(Dockerfile)
class ExtendDockerfile:
    service = P.parent(Service, "has", "dockerfile")
    templates = "templates_{{res.term.data}}"
    output_dir = output_dir_from("service")


@extend(Service)
class ExtendService:
    dockerfile = P.child("has", ":dockerfile")
    dockerfile_dev = P.child("has", "dev:dockerfile")
