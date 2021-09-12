from moonleap import add, rule

from . import docker_compose_configs, dodo_layer_configs


@rule("docker-image")
def node_docker_image_created(docker_image):
    if docker_image.name.startswith("node:"):
        docker_image.install_command = "apk update && apk add"
        add(docker_image, docker_compose_configs.get(docker_image))
        add(docker_image, dodo_layer_configs.get())
