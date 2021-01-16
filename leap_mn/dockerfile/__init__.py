import moonleap.resource.props as P
from leap_mn.service import Service
from moonleap import StoreOutputPaths, extend, render_templates, rule, tags

from .resources import Dockerfile


@tags(["dockerfile"])
def create_dockerfile(term, block):
    docker_file = Dockerfile(is_dev=term.data == "dev")
    return docker_file


@rule("dockerfile", "use", "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    dockerfile.image_name = docker_image.term.data


def get_template_filename(dockerfile):
    return "templates/Dockerfile" + (".dev" if dockerfile.is_dev else "")


@extend(Dockerfile)
class ExtendDockerfile(StoreOutputPaths):
    service = P.parent(Service, "has", "dockerfile")
    render = render_templates(__file__, get_template_filename)
