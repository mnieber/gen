from moonleap import install

from . import (
    appmodule,
    appstore,
    flags,
    graphqlapi,
    itemlist,
    itemtype,
    loaditemseffect,
    policy,
    store,
    storeprovider,
    utilsmodule,
)


def install_all():
    install(appmodule)
    install(appstore)
    install(flags)
    install(graphqlapi)
    install(itemlist)
    install(itemtype)
    install(loaditemseffect)
    install(policy)
    install(store)
    install(storeprovider)
    install(utilsmodule)
