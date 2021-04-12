from moonleap import rule
from moonleap.verbs import has


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
