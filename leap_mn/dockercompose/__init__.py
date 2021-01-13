import moonleap.props as P
from leap_mn.layerconfig import LayerConfig
from leap_mn.project import Project
from moonleap import extend, output_dir_from, rule, tags

from .layer_configs import get_layer_config
from .resources import DockerCompose


@tags(["docker-compose"])
def create_docker_compose(term, block):
    docker_compose = DockerCompose()
    return docker_compose


@tags(["dev:docker-compose"])
def create_docker_compose_dev(term, block):
    docker_compose_dev = DockerCompose(is_dev=True)
    return docker_compose_dev


@rule(
    "project",
    "has",
    "docker-compose",
    description="""
Add docker-compose settings to the root config layer in the dodo configuration.""",
)
def project_has_docker_compose(project, docker_compose):
    layer_config = LayerConfig(lambda: get_layer_config(docker_compose))
    project.config_layer.add_to_layer_configs(layer_config)


@extend(DockerCompose)
class ExtendDockerCompose:
    output_dir = output_dir_from("project")
    templates = "templates"
    services = P.children("run", "service")
    project = P.parent(Project, "has", "docker-compose")


def meta():
    return [ExtendDockerCompose]
