import moonleap.resource.props as P
from moonleap import (
    MemFun,
    StoreOutputPaths,
    extend,
    register_add,
    render_templates,
    tags,
)
from moonleap.verbs import has
from titan.project_pkg.service import Tool

from . import props
from .resources import DockerCompose, DockerComposeConfig  # noqa


class StoreDockerComposeConfigs:
    docker_compose_configs = P.tree(has, "docker-compose-config")


@register_add(DockerComposeConfig)
def add_docker_compose_config(resource, docker_compose_config):
    resource.docker_compose_configs.add(docker_compose_config)


@tags(["docker-compose"])
def create_docker_compose(term, block):
    docker_compose = DockerCompose()
    return docker_compose


@extend(DockerCompose)
class ExtendDockerCompose(StoreOutputPaths):
    render = MemFun(render_templates(__file__))
    get_config = MemFun(props.get_docker_compose_config)


@extend(Tool)
class ExtendTool(StoreDockerComposeConfigs):
    pass
