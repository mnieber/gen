from pathlib import Path

from titan.project_pkg.project import Project

import moonleap.packages.extensions.props as P
from moonleap import create, extend, rule
from moonleap.blocks.verbs import has, runs

from .resources import DockerCompose  # noqa


@create("docker-compose")
def create_docker_compose(term):
    return DockerCompose()


@rule("project", has, "docker-compose")
def project_renders_docker_compose_file(project, docker_compose):
    project.renders(
        [docker_compose],
        "",
        dict(docker_compose=docker_compose),
        [Path(__file__).parent / "templates"],
    )


@rule("docker-compose", runs, "service")
def service_adds_to_docker_compose_file(docker_compose, service):
    service.renders(
        [docker_compose],
        "",
        dict(docker_compose=docker_compose),
        [Path(__file__).parent / "templates_service"],
    )


@extend(DockerCompose)
class ExtendDockerCompose:
    services = P.children(
        runs, "service", lambda services: sorted(services, key=lambda x: x.name)
    )
    project = P.parent("project", has)


@extend(Project)
class ExtendProject:
    docker_compose = P.child(has, "docker-compose")
