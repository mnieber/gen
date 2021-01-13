import moonleap.props as P
from leap_mn.layer import LayerConfig, StoreLayerConfigs
from leap_mn.project import Project
from moonleap import extend, output_dir_from, rule, tags

from . import layer_configs as LC
from .props import docker_compose_config_prop
from .resources import DockerCompose, DockerComposeConfig


@tags(["docker-compose"])
def create_docker_compose(term, block):
    docker_compose = DockerCompose(is_dev=term.data == "dev")
    docker_compose.add_to_layer_configs(
        LayerConfig(lambda: LC.get_docker_compose_options(docker_compose))
    )
    return docker_compose


@rule(
    "project",
    "has",
    "docker-compose",
    description="""
Add docker-compose dodo settings to the project.""",
)
def project_has_docker_compose(project, docker_compose):
    if not docker_compose.configured_by_layer:
        project.add_to_layer_config_sources(docker_compose)


@rule(
    "docker-compose",
    "configured",
    "layer",
    description="""
Docker-compose is configured in its own layer.""",
)
def docker_compose_configured_in_layer(docker_compose, layer):
    layer.add_to_layer_config_sources(docker_compose)


class StoreDockerComposeConfigs:
    docker_compose_config = docker_compose_config_prop()
    docker_compose_configs = P.children("has", "docker-compose-config")
    docker_compose_config_sources = P.children("has", "docker-compose-config-source")


@extend(DockerCompose)
class ExtendDockerCompose(StoreLayerConfigs, StoreDockerComposeConfigs):
    output_dir = output_dir_from("project")
    templates = "templates"
    services = P.children("run", "service")
    project = P.parent(Project, "has", "docker-compose")
    configured_by_layer = P.child("configured", "layer")
