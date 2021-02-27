from moonleap import install

from . import (
    appmodule,
    appstore,
    flags,
    graphqlapi,
    item,
    itemlist,
    itemtype,
    store,
    storeprovider,
    utilsmodule,
)


def install_all():
    install(appmodule)
    install(appstore)
    install(flags)
    install(graphqlapi)
    install(item)
    install(itemlist)
    install(itemtype)
    install(store)
    install(storeprovider)
    install(utilsmodule)
