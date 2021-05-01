from moonleap import install

from . import (
    api,
    appmodule,
    appstore,
    constantsapi,
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
    install(api)
    install(appmodule)
    install(appstore)
    install(constantsapi)
    install(flags)
    install(graphqlapi)
    install(itemlist)
    install(itemtype)
    install(loaditemseffect)
    install(policy)
    install(store)
    install(storeprovider)
    install(utilsmodule)
