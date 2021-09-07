import moonleap.resource.props as P
from moonleap import add_src_inv, extend
from moonleap.verbs import has
from titan.project_pkg.dockercompose.resources import DockerCompose
from titan.project_pkg.project import Project

rules = [(("project", has, "docker-compose"), add_src_inv("output_paths"))]


@extend(DockerCompose)
class ExtendDockerCompose:
    project = P.parent(Project, has)


@extend(Project)
class ExtendProject:
    docker_compose = P.child(has, "docker-compose")
