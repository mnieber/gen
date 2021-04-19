import os

from moonleap import install

from . import behavior, behavior_and_module, container, containerprovider


def install_all():
    install(container)
    install(containerprovider)
    install(behavior)
    install(behavior_and_module)
