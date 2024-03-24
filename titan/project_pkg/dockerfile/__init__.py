import moonleap.extension.props as P
from moonleap import create, extend, rule
from moonleap.spec.verbs import has

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


def set_dockerfile_image_name(dockerfile, docker_image):
    dockerfile.image_name = docker_image.name


@extend(Dockerfile)
class ExtendDockerfile:
    docker_image = P.child(has, "docker-image")


rules = {
    "dockerfile": {
        (has, "docker-image"): (
            #
            set_dockerfile_image_name
        )
    },
}
