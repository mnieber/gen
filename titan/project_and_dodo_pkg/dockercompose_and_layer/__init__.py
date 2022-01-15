from pathlib import Path

import moonleap.resource.props as P
from moonleap import add, extend, feeds, receives, rule
from moonleap.verbs import configured_by, has
from titan.dodo_pkg.layer import StoreLayerConfigs
from titan.project_pkg.dockercompose.resources import DockerCompose

from . import dodo_layer_configs

rules = [(("docker-compose", configured_by, "layer"), feeds("dodo_layer_configs"))]


@rule("docker-compose")
def docker_compose_created(docker_compose):
    add(docker_compose, dodo_layer_configs.get(docker_compose))


@rule("project", has, "docker-compose")
def project_has_docker_compose(project, docker_compose):
    if not docker_compose.configured_by_layer:
        receives("dodo_layer_configs")(project, docker_compose)


@rule("project", has, "docker-compose")
def add_docker_compose_override_to_ignore(project, docker_compose):
    project.add_template_dir(Path(__file__).parent / "templates_project")


@extend(DockerCompose)
class ExtendDockerCompose(StoreLayerConfigs):
    configured_by_layer = P.child(configured_by, "layer")
