import moonleap.resource.props as P
from moonleap import extend
from moonleap.verbs import has
from moonleap_project.dockercompose.resources import DockerCompose
from moonleap_project.project import Project


@extend(DockerCompose)
class ExtendDockerCompose:
    project = P.parent(Project, has, "docker-compose")


@extend(Project)
class ExtendProject:
    docker_compose = P.child(has, "docker-compose")
