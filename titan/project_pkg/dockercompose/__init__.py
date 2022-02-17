from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    StoreOutputPaths,
    StoreTemplateDirs,
    create,
    extend,
    register_add,
)
from titan.project_pkg.service import Tool

from . import props
from .resources import DockerCompose, DockerComposeConfig  # noqa


class StoreDockerComposeConfigs:
    docker_compose_configs = P.tree("docker_compose_configs")


@register_add(DockerComposeConfig)
def add_docker_compose_config(resource, docker_compose_config):
    resource.docker_compose_configs.add(docker_compose_config)


@create("docker-compose")
def create_docker_compose(term):
    docker_compose = DockerCompose()
    docker_compose.add_template_dir(Path(__file__).parent / "templates")
    return docker_compose


@extend(DockerCompose)
class ExtendDockerCompose(StoreOutputPaths, StoreTemplateDirs):
    get_config = MemFun(props.get_docker_compose_config)


@extend(Tool)
class ExtendTool(StoreDockerComposeConfigs):
    pass
