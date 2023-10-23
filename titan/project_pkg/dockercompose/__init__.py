import moonleap.packages.extensions.props as P
from moonleap import create, empty_rule, extend
from moonleap.blocks.verbs import has, runs
from titan.project_pkg.project import Project

from .resources import DockerCompose  # noqa


@create("docker-compose")
def create_docker_compose(term):
    return DockerCompose()


@extend(DockerCompose)
class ExtendDockerCompose:
    services = P.children(
        runs, "service", lambda services: sorted(services, key=lambda x: x.name)
    )
    project = P.parent("project", has)


@extend(Project)
class ExtendProject:
    docker_compose = P.child(has, "docker-compose")


rules = {
    "project": {
        (has, "docker-compose"): empty_rule(),
    },
    "docker-compose": {
        (runs, "service"): empty_rule(),
    },
}
