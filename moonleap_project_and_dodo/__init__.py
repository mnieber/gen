from moonleap import install

from . import (
    configlayer,
    dockercompose_and_layer,
    project_and_layer,
    service_and_layer,
    service_and_layergroup,
    vscodeproject_and_layer,
)


def install_all():
    install(configlayer)
    install(dockercompose_and_layer)
    install(project_and_layer)
    install(service_and_layer)
    install(service_and_layergroup)
    install(vscodeproject_and_layer)
