import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from moonleap_project.dockercompose.resources import DockerCompose
from moonleap_project.project import Project


@rule("project", has, "docker-compose")
def project_has_docker_compose(project, docker_compose):
    docker_compose.output_paths.add_source(project)


@extend(DockerCompose)
class ExtendDockerCompose:
    project = P.parent(Project, has)


@extend(Project)
class ExtendProject:
    docker_compose = P.child(has, "docker-compose")
