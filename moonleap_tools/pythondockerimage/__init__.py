from moonleap import add, create_forward, rule
from moonleap.verbs import has

from . import docker_compose_configs, layer_configs

custom_steps_dev = """# create a python venv that we can easily store inside a docker volume
RUN python3 -m venv /app/env
ENV PATH="/app/env/bin:${PATH}"
"""

custom_steps_pre_dev = """RUN pip install --upgrade pip
"""

custom_steps_pre = """RUN pip install --upgrade pip
"""


@rule("docker-image")
def python_docker_image_created(docker_image):
    if docker_image.name.startswith("python:"):
        add(docker_image, docker_compose_configs.get(docker_image))
        add(docker_image, layer_configs.get())


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    if docker_image.name.startswith("python:"):
        dockerfile.custom_steps_pre_dev += custom_steps_pre_dev
        dockerfile.custom_steps_dev += custom_steps_dev
        dockerfile.custom_steps_pre += custom_steps_pre


@rule("dockerfile", has, "docker-image")
def add_makefile_to_service(dockerfile, docker_image):
    if docker_image.name.startswith("python:"):
        return create_forward(dockerfile.service, has, ":makefile")
