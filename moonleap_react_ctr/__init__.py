import os

from moonleap import install

from . import (
    behavior,
    behavior_and_module,
    container,
    containerprovider,
    itemview,
    listview,
    picker,
)


def install_all():
    install(behavior)
    install(behavior_and_module)
    install(container)
    install(containerprovider)
    install(itemview)
    install(listview)
    install(picker)
