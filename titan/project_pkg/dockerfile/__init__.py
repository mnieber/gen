import moonleap.resource.props as P
from moonleap import RenderTemplates, add_src, create, extend, rule
from moonleap.verbs import has

from .resources import Dockerfile, DockerImage

rules = [(("dockerfile", has, "docker-image"), add_src("docker_compose_configs"))]


@create(["dockerfile"])
def create_dockerfile(term, block):
    docker_file = Dockerfile(is_dev=term.data == "dev", name="dockerfile")
    return docker_file


@create(["docker-image"])
def create_docker_image(term, block):
    docker_image = DockerImage(term.data)
    return docker_image


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    dockerfile.image_name = docker_image.name


@extend(Dockerfile)
class ExtendDockerfile(RenderTemplates(__file__)):
    docker_image = P.child(has, "docker-image")
