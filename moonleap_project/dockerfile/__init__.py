import moonleap.resource.props as P
from moonleap import MemFun, add_source, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.service import Service

from .resources import Dockerfile, DockerImage


@tags(["dockerfile"])
def create_dockerfile(term, block):
    docker_file = Dockerfile(is_dev=term.data == "dev", name="dockerfile")
    return docker_file


@tags(["docker-image"])
def create_docker_image(term, block):
    docker_image = DockerImage(term.data)
    return docker_image


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    dockerfile.image_name = docker_image.name
    add_source(
        [dockerfile, "docker_compose_configs"],
        docker_image,
        "A :dockerfile receives docker compose configs from a :docker-image",
    )


@extend(Dockerfile)
class ExtendDockerfile:
    service = P.parent(Service, has)
    render = MemFun(render_templates(__file__))
    docker_image = P.child(has, "docker-image")
