from moonleap import install

from . import (
    appmodule,
    appstore,
    flags,
    graphqlapi,
    itemlist,
    itemtype,
    loaditemseffect,
    selectitemeffect,
    store,
    storeprovider,
    utilsmodule,
)


def install_all():
    install(appmodule)
    install(appstore)
    install(loaditemseffect)
    install(flags)
    install(graphqlapi)
    install(itemlist)
    install(itemtype)
    install(selectitemeffect)
    install(store)
    install(storeprovider)
    install(utilsmodule)
