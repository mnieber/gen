import moonleap.extension.props as P
from moonleap import create, create_forward, empty_rule, extend, kebab_to_camel
from moonleap.spec.verbs import configured_by, contains, has
from titan.project_pkg.dockercompose.resources import DockerCompose
from titan.project_pkg.project import Project
from titan.project_pkg.service import Service

from .resources import DodoLayer


@create("layer")
def create_layer(term):
    name = kebab_to_camel(term.data)
    return DodoLayer(name=name, is_root=name == "config")


@extend(DockerCompose)
class ExtendDockerCompose:
    configured_by_layer = P.child(configured_by, "layer")


@extend(Project)
class ExtendProject:
    config_layer = P.child(has, "config:layer")
    layers = P.children(has, "layer")


@extend(Service)
class ExtendService:
    layer = P.child(configured_by, "layer")


@extend(DodoLayer)
class ExtendDodoLayer:
    configures_docker_compose = P.parent("docker-compose", configured_by)
    dodo_menu = P.child(contains, "dodo-menu")
    configures_service = P.parent("service", configured_by)


rules = {
    "layer": {
        (contains, "dodo-menu"): empty_rule(),
    },
    "docker-compose": {
        (configured_by, "layer"): (
            # then project has layer
            lambda docker_compose, layer: create_forward(
                docker_compose.project, has, layer
            )
        )
    },
    "service": {
        (configured_by, "layer"): (
            # then project has layer
            lambda service, layer: create_forward(service.project, has, layer)
        )
    },
    "project": {(has, "layer"): empty_rule()},
}
