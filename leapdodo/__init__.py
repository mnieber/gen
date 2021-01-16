from moonleap import install

from . import layer, layergroup


def install_all():
    install(layer)
    install(layergroup)
