import moonleap.resource.props as P
from moonleap import add, add_source, extend, rule
from moonleap.verbs import configured_by, has
from moonleap_dodo.layer import StoreLayerConfigs
from moonleap_project.dockercompose.resources import DockerCompose

from . import layer_configs


@rule("docker-compose")
def docker_compose_created(docker_compose):
    add(docker_compose, layer_configs.get(docker_compose))


@rule("docker-compose", configured_by, "layer")
def docker_compose_configured_in_layer(docker_compose, layer):
    add_source(
        [layer, "layer_configs"],
        docker_compose,
        "The :layer receives layer configs from a :docker-compose",
    )


@rule("project", has, "docker-compose")
def project_has_docker_compose(project, docker_compose):
    if not docker_compose.configured_by_layer:
        project.layer_configs.add_source(docker_compose)


@extend(DockerCompose)
class ExtendDockerCompose(StoreLayerConfigs):
    configured_by_layer = P.child(configured_by, "layer")
