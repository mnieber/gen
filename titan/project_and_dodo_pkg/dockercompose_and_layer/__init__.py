import moonleap.resource.props as P
from moonleap import add, add_src_inv, extend, rule
from moonleap.verbs import configured_by, has
from titan.dodo_pkg.layer import StoreLayerConfigs
from titan.project_pkg.dockercompose.resources import DockerCompose

from . import dodo_layer_configs

rules = [
    (("docker-compose", configured_by, "layer"), add_src_inv("dodo_layer_configs"))
]


@rule("docker-compose")
def docker_compose_created(docker_compose):
    add(docker_compose, dodo_layer_configs.get(docker_compose))


@rule("project", has, "docker-compose")
def project_has_docker_compose(project, docker_compose):
    if not docker_compose.configured_by_layer:
        project.dodo_layer_configs.add_source(docker_compose)


@extend(DockerCompose)
class ExtendDockerCompose(StoreLayerConfigs):
    configured_by_layer = P.child(configured_by, "layer")
