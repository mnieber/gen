from moonleap import install

from . import (
    behavior,
    container,
    containerprovider,
    highlightbvr,
    itemview,
    listview,
    picker,
    selectionbvr,
)


def install_all():
    install(behavior)
    install(container)
    install(containerprovider)
    install(highlightbvr)
    install(itemview)
    install(listview)
    install(picker)
    install(selectionbvr)
