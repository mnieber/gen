import moonleap.resource.props as P
from leapdodo.layer import LayerConfig, StoreLayerConfigs
from leapproject.project import Project
from moonleap import MemFun, StoreOutputPaths, extend, render_templates, rule, tags

from . import layer_configs as LC
from . import props
from .resources import DockerCompose, DockerComposeConfig  # noqa

configured = "configured"


@tags(["docker-compose"])
def create_docker_compose(term, block):
    docker_compose = DockerCompose(is_dev=term.data == "dev")
    docker_compose.layer_configs.add(
        LayerConfig(lambda x: LC.get_docker_compose_options(docker_compose))
    )
    return docker_compose


@rule(
    "docker-compose",
    configured,
    "layer",
    description="""
Docker-compose is configured in its own layer.""",
)
def docker_compose_configured_in_layer(docker_compose, layer):
    layer.layer_configs.add_source(docker_compose)


class StoreDockerComposeConfigs:
    docker_compose_configs = P.tree("has", "docker-compose-config")


@extend(DockerCompose)
class ExtendDockerCompose(StoreLayerConfigs, StoreOutputPaths):
    render = render_templates(__file__)
    services = P.children("run", "service")
    project = P.parent(Project, "has", "docker-compose")
    configured_by_layer = P.child("configured", "layer")
    get_config = MemFun(props.get_docker_compose_config)
