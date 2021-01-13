import moonleap.props as P
from leap_mn.layer import LayerConfig
from leap_mn.project import Project
from moonleap import extend, output_dir_from, rule, tags

from . import layer_configs as LC
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
Add docker-compose dodo settings to the project.""",
)
def project_has_docker_compose(project, docker_compose):
    project.add_to_layer_configs(
        LayerConfig(lambda: LC.get_docker_compose_options(docker_compose))
    )


@extend(DockerCompose)
class ExtendDockerCompose:
    output_dir = output_dir_from("project")
    templates = "templates"
    services = P.children("run", "service")
    project = P.parent(Project, "has", "docker-compose")
