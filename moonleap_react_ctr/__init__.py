from moonleap import install

from . import (
    behavior,
    container,
    containerprovider,
    highlightbehavior,
    itemview,
    listview,
    picker,
    selectionbehavior,
)


def install_all():
    install(behavior)
    install(container)
    install(containerprovider)
    install(highlightbehavior)
    install(itemview)
    install(listview)
    install(picker)
    install(selectionbehavior)
