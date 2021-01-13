import moonleap.props as P
from leap_mn.layerconfig import LayerConfig
from leap_mn.service import Service
from moonleap import extend, output_dir_from, rule, tags

from .layer_configs import get_layer_config
from .resources import Dockerfile


@tags(["dockerfile"])
def create_dockerfile(term, block):
    docker_file = Dockerfile()
    docker_file.layer_config = LayerConfig(
        lambda: dict(DOCKER_OPTIONS=get_layer_config(docker_file))
    )
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
If the service has a dodo layer then we add the docker options to that layer.""",
)
def service_has_dockerfile(service, dockerfile):
    if service.layer:
        layer_config = LayerConfig(lambda: get_layer_config(service))
        service.layer.add_to_layer_configs(layer_config)


@extend(Dockerfile)
class ExtendDockerfile:
    service = P.parent(Service, "has", "dockerfile")
    templates = "templates_{{res.term.data}}"
    output_dir = output_dir_from("service")


@extend(Service)
class ExtendService:
    dockerfile = P.child("has", ":dockerfile")
    dockerfile_dev = P.child("has", "dev:dockerfile")


def meta():
    return [ExtendDockerfile, ExtendService]
