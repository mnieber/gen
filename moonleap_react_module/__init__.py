from moonleap import install

from . import (
    apimodule,
    appmodule,
    appstore,
    flags,
    graphqlapi,
    item,
    itemlist,
    itemtype,
    loaditemeffect,
    loaditemseffect,
    mockgraphqlserver,
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
    install(item)
    install(itemlist)
    install(itemtype)
    install(loaditemeffect)
    install(loaditemseffect)
    install(mockgraphqlserver)
    install(policy)
    install(store)
    install(storeprovider)
    install(utilsmodule)
