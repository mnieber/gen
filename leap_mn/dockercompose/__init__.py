import moonleap.resource.props as P
from leap_mn.layer import LayerConfig, StoreLayerConfigs
from leap_mn.outputpath import StoreOutputPaths
from leap_mn.project import Project
from moonleap import MemFun, extend, render_templates, rule, tags

from . import layer_configs as LC
from . import props
from .resources import DockerCompose, DockerComposeConfig  # noqa


@tags(["docker-compose"])
def create_docker_compose(term, block):
    docker_compose = DockerCompose(is_dev=term.data == "dev")
    docker_compose.layer_configs.add(
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
        project.layer_configs.add_source(docker_compose)
    docker_compose.output_paths.add_source(project)


@rule(
    "docker-compose",
    "configured",
    "layer",
    description="""
Docker-compose is configured in its own layer.""",
)
def docker_compose_configured_in_layer(docker_compose, layer):
    layer.layer_configs.add_source(docker_compose)


class StoreDockerComposeConfigs:
    docker_compose_configs = P.tree(
        "has",
        "docker-compose-config",
        merge=lambda acc, x: [*acc, x],
        initial=list(),
    )
    get_docker_compose_config = MemFun(props.get_docker_compose_config)


@extend(DockerCompose)
class ExtendDockerCompose(StoreLayerConfigs, StoreOutputPaths):
    render = render_templates(__file__)
    services = P.children("run", "service")
    project = P.parent(Project, "has", "docker-compose")
    configured_by_layer = P.child("configured", "layer")
