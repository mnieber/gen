from moonleap import install

from . import (
    apimodule,
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
    install(apimodule)
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
