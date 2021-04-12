from moonleap import install

from . import (
    configlayer,
    dockercompose,
    dockercompose_and_layer,
    dockercompose_and_project,
    dockercompose_and_service,
    dockerfile,
    project,
    project_and_dockercompose,
    project_and_layer,
    project_and_service,
    service,
    service_and_docker,
    service_and_layergroup,
    srcdir,
    vscodeproject,
)


def install_all():
    install(configlayer)
    install(dockercompose)
    install(dockercompose_and_layer)
    install(dockercompose_and_project)
    install(dockercompose_and_service)
    install(dockerfile)
    install(project)
    install(project_and_dockercompose)
    install(project_and_layer)
    install(project_and_service)
    install(service)
    install(service_and_docker)
    install(service_and_layergroup)
    install(srcdir)
    install(vscodeproject)
