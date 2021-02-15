from moonleap import install

from . import (
    appmodule,
    appstore,
    graphqlapi,
    itemlist,
    store,
    storeprovider,
    utilsmodule,
)


def install_all():
    install(appmodule)
    install(appstore)
    install(graphqlapi)
    install(itemlist)
    install(store)
    install(storeprovider)
    install(utilsmodule)
