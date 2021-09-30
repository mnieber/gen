import moonleap.resource.props as P
from moonleap import extend, feeds
from moonleap.verbs import has
from titan.project_pkg.dockercompose.resources import DockerCompose
from titan.project_pkg.project import Project

rules = [(("project", has, "docker-compose"), feeds("output_paths"))]


@extend(DockerCompose)
class ExtendDockerCompose:
    project = P.parent("project", has, required=True)


@extend(Project)
class ExtendProject:
    docker_compose = P.child(has, "docker-compose")
