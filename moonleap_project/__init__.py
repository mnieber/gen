from moonleap import install

from . import (
    dockercompose,
    dockercompose_and_project,
    dockercompose_and_service,
    dockerfile,
    project,
    project_and_service,
    service,
    service_and_docker,
    srcdir,
    vscodeproject,
)


def install_all():
    install(dockercompose)
    install(dockercompose_and_project)
    install(dockercompose_and_service)
    install(dockerfile)
    install(project)
    install(project_and_service)
    install(service)
    install(service_and_docker)
    install(srcdir)
    install(vscodeproject)
