import os

from moonleap import install

from . import behavior, container


def install_all():
    install(container)
    install(behavior)
