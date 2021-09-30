from pathlib import Path

import moonleap.resource.props as P
from moonleap import StoreTemplateDirs, receives, create, extend, rule
from moonleap.verbs import has

from .resources import Dockerfile, DockerImage

rules = [(("dockerfile", has, "docker-image"), receives("docker_compose_configs"))]


base_tags = [
    ("dockerfile", ["tool"]),
    ("docker-image", ["tool"]),
]


@create("dockerfile")
def create_dockerfile(term, block):
    docker_file = Dockerfile(is_dev=term.data == "dev", name="dockerfile")
    docker_file.add_template_dir(Path(__file__).parent / "templates")
    return docker_file


@create("docker-image")
def create_docker_image(term, block):
    docker_image = DockerImage(term.data)
    return docker_image


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    dockerfile.image_name = docker_image.name


@extend(Dockerfile)
class ExtendDockerfile(StoreTemplateDirs):
    docker_image = P.child(has, "docker-image")
