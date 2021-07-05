import moonleap.resource.props as P
from moonleap import (MemFun, StoreOutputPaths, extend, register_add,
                      render_templates, rule, tags)
from moonleap.verbs import has

from . import props
from .resources import DockerCompose, DockerComposeConfig  # noqa


@register_add(DockerComposeConfig)
def add_docker_compose_config(resource, docker_compose_config):
    resource.docker_compose_configs.add(docker_compose_config)


class StoreDockerComposeConfigs:
    docker_compose_configs = P.tree(has, "docker-compose-config")


@tags(["docker-compose"])
def create_docker_compose(term, block):
    docker_compose = DockerCompose()
    return docker_compose


@rule("project", has, "docker-compose")
def project_has_docker_compose(project, docker_compose):
    docker_compose.output_paths.add_source(project)


@extend(DockerCompose)
class ExtendDockerCompose(StoreOutputPaths):
    render = MemFun(render_templates(__file__))
    get_config = MemFun(props.get_docker_compose_config)
