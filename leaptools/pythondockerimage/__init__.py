from moonleap import add, created

from . import docker_compose_configs, layer_configs


@created("docker-image")
def python_docker_image_created(docker_image):
    if docker_image.name.startswith("python:"):
        add(docker_image, docker_compose_configs.get(docker_image))
        add(docker_image, layer_configs.get())
