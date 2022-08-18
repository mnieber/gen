from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, extend, rule
from moonleap.verbs import has, runs
from titan.project_pkg.project import Project

from .resources import DockerCompose  # noqa


@create("docker-compose")
def create_docker_compose(term):
    return DockerCompose()


@rule("project", has, "docker-compose")
def project_has_docker_compose(project, docker_compose):
    project.renders(
        [docker_compose],
        "",
        dict(docker_compose=docker_compose),
        [Path(__file__).parent / "templates"],
    )


@rule("docker-compose", runs, "service")
def docker_compose_runs_service(docker_compose, service):
    service.renders(
        [docker_compose],
        "",
        dict(docker_compose=docker_compose),
        [Path(__file__).parent / "templates_service"],
    )


@extend(DockerCompose)
class ExtendDockerCompose:
    services = P.children(runs, "service")
    project = P.parent("project", has)


@extend(Project)
class ExtendProject:
    docker_compose = P.child(has, "docker-compose")
