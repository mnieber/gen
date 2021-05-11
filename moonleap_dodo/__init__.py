from moonleap import install

from . import layer, layer_and_layergroup, layergroup


def install_all():
    install(layer)
    install(layergroup)
    install(layer_and_layergroup)
