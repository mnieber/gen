from moonleap import install

from . import layer, layergroup, service_and_layer


def install_all():
    install(layer)
    install(service_and_layer)
    install(layergroup)
