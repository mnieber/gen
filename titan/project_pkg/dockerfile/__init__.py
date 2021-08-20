import moonleap.resource.props as P
from moonleap import RenderTemplates, add_source, extend, rule, tags
from moonleap.verbs import has

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
class ExtendDockerfile(RenderTemplates(__file__)):
    docker_image = P.child(has, "docker-image")
