from moonleap import install

from . import (
    appmodule,
    appstore,
    flags,
    graphqlapi,
    item,
    itemlist,
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
    install(store)
    install(storeprovider)
    install(utilsmodule)
