import os

from moonleap import install

from . import (
    behavior,
    container,
    containerprovider,
    itemview,
    listview,
    picker,
    selectionbehavior,
)


def install_all():
    install(behavior)
    install(container)
    install(containerprovider)
    install(itemview)
    install(listview)
    install(picker)
    install(selectionbehavior)
