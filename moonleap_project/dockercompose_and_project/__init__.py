import moonleap.resource.props as P
from moonleap import extend
from moonleap_project.dockercompose.resources import DockerCompose
from moonleap_project.project import Project


@extend(DockerCompose)
class ExtendDockerCompose:
    project = P.parent(Project, "has", "docker-compose")
