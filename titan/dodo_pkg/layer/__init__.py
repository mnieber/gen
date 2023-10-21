from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import (
    create,
    create_forward,
    empty_rule,
    extend,
    get_root_resource,
    kebab_to_camel,
    rule,
)
from moonleap.blocks.verbs import configured_by, contains, has
from titan.project_pkg.dockercompose.resources import DockerCompose
from titan.project_pkg.project import Project
from titan.project_pkg.service import Service

from .resources import DodoLayer

rules = {
    ("layer", contains, "dodo-menu"): empty_rule(),
}


@create("layer")
def create_layer(term):
    name = kebab_to_camel(term.data)
    return DodoLayer(name=name, is_root=name == "config")


@rule("docker-compose", configured_by, "layer")
def docker_compose_configured_by_layer(docker_compose, layer):
    return create_forward(docker_compose.project, has, layer)


@rule("service", configured_by, "layer")
def service_configured_by_layer(service, layer):
    return create_forward(service.project, has, layer)


@extend(DockerCompose)
class ExtendDockerCompose:
    configured_by_layer = P.child(configured_by, "layer")


@extend(Project)
class ExtendProject:
    config_layer = P.child(has, "config:layer")


@extend(Service)
class ExtendService:
    layer = P.child(configured_by, "layer")


@extend(DodoLayer)
class ExtendDodoLayer:
    configures_docker_compose = P.parent("docker-compose", configured_by)
    dodo_menu = P.child(contains, "dodo-menu")
    configures_service = P.parent("service", configured_by)
