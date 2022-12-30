import moonleap.packages.extensions.props as P
from moonleap import create, extend, rule
from moonleap.blocks.verbs import has

from .resources import Dockerfile, DockerImage

base_tags = {
    "dockerfile": ["tool"],
    "docker-image": ["tool"],
}


@create("dockerfile")
def create_dockerfile(term):
    docker_file = Dockerfile(
        target="dev" if term.data == "dev" else "prod", name="dockerfile"
    )
    return docker_file


@create("docker-image")
def create_docker_image(term):
    docker_image = DockerImage(term.data)
    return docker_image


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    dockerfile.image_name = docker_image.name


@extend(Dockerfile)
class ExtendDockerfile:
    docker_image = P.child(has, "docker-image")
