from moonleap import install

from . import layer, layer_and_layergroup, layergroup, service_and_layer


def install_all():
    install(layer)
    install(service_and_layer)
    install(layergroup)
    install(layer_and_layergroup)
