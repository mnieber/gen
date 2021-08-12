from moonleap import rule, tags
from moonleap.verbs import uses
from titan.project_pkg.dockerfile import create_docker_image

custom_steps_pre_dev = """ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
"""


@tags(["strapi:docker-image"])
def strapi_docker_image_created(term, block):
    docker_image = create_docker_image(term, block)
    docker_image.name = "strapi/strapi"
    docker_image.install_command = "apt-get update && apt-get install -y"
    return docker_image


@rule("dockerfile", uses, "docker-image")
def strapi_docker_image_used(dockerfile, docker_image):
    if docker_image.name == "strapi/strapi":
        dockerfile.custom_steps_pre_dev += custom_steps_pre_dev
