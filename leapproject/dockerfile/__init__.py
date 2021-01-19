import moonleap.resource.props as P
from leapproject.service import Service
from moonleap import StoreOutputPaths, extend, render_templates, rule, tags
from moonleap.verbs import has

from .resources import Dockerfile, DockerImage


@tags(["dockerfile"])
def create_dockerfile(term, block):
    docker_file = Dockerfile(is_dev=term.data == "dev")
    return docker_file


@tags(["docker-image"])
def create_docker_image(term, block):
    docker_image = DockerImage(term.data)
    return docker_image


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    dockerfile.image_name = docker_image.term.data


def get_template_filename(dockerfile):
    return "templates/Dockerfile" + (".dev" if dockerfile.is_dev else "")


@extend(Dockerfile)
class ExtendDockerfile(StoreOutputPaths):
    service = P.parent(Service, has, "dockerfile")
    render = render_templates(__file__, get_template_filename)
