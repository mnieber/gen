import moonleap.resource.props as P
from moonleap import MemFun, StoreOutputPaths, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.dockercompose import StoreDockerComposeConfigs
from moonleap_project.service import Service

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
    dockerfile.docker_compose_configs.add_source(docker_image)


def get_template_filename(dockerfile):
    return "templates/Dockerfile" + (".dev" if dockerfile.is_dev else "") + ".j2"


@extend(DockerImage)
class ExtendDockerImage(StoreDockerComposeConfigs):
    dockerfile = P.parent(Dockerfile, has, "docker-image")


@extend(Dockerfile)
class ExtendDockerfile(StoreOutputPaths, StoreDockerComposeConfigs):
    service = P.parent(Service, has, "dockerfile")
    render = MemFun(render_templates(__file__, get_template_filename))
