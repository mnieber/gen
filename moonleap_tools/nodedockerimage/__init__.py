from moonleap import add, create_forward, rule
from moonleap.verbs import has

from . import docker_compose_configs, layer_configs, makefile_rules


@rule("docker-image")
def node_docker_image_created(docker_image):
    if docker_image.name.startswith("node:"):
        docker_image.install_command = "apk update && apk add"
        add(docker_image, docker_compose_configs.get(docker_image))
        add(docker_image, layer_configs.get())
        add(docker_image, makefile_rules.get())


@rule("dockerfile", has, "docker-image")
def add_makefile_to_service(dockerfile, docker_image):
    if docker_image.name.startswith("node:"):
        return create_forward(dockerfile.service, has, ":makefile")
