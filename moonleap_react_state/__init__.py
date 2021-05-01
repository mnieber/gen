from moonleap import install

from . import (
    behavior,
    highlightbvr,
    itemview,
    listview,
    picker,
    selectionbvr,
    selectitemeffect,
    state,
    stateprovider,
)


def install_all():
    install(behavior)
    install(state)
    install(stateprovider)
    install(highlightbvr)
    install(itemview)
    install(listview)
    install(picker)
    install(selectionbvr)
    install(selectitemeffect)
