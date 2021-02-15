import moonleap.resource.props as P
from moonleap_dodo.layer import StoreLayerConfigs
from moonleap import StoreOutputPaths, extend, rule, tags
from moonleap.verbs import has

from .resources import Project


@tags(["project"])
def create_project(term, block):
    project = Project(term.data)
    project.output_path = "src/"
    return project


@rule("project", has, "service")
def project_has_service(project, service):
    service.output_paths.add_source(project)


@rule("project", has, "config:layer")
def project_has_config_layer(project, config_layer):
    config_layer.layer_configs.add_source(project)


@rule(
    "project",
    has,
    "docker-compose",
    description="""
Add docker-compose dodo settings to the project.""",
)
def project_has_docker_compose(project, docker_compose):
    if not docker_compose.configured_by_layer:
        project.layer_configs.add_source(docker_compose)
    docker_compose.output_paths.add_source(project)


@extend(Project)
class ExtendProject(StoreLayerConfigs, StoreOutputPaths):
    services = P.child(has, "service")
    src_dir = P.child(has, "src-dir")
    config_layer = P.child(has, "config:layer", is_doc=False)
