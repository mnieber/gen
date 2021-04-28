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
    selectitemeffect,
    store,
    storeprovider,
    utilsmodule,
)


def install_all():
    install(api)
    install(appmodule)
    install(appstore)
    install(constantsapi)
    install(loaditemseffect)
    install(flags)
    install(graphqlapi)
    install(itemlist)
    install(itemtype)
    install(selectitemeffect)
    install(store)
    install(storeprovider)
    install(utilsmodule)
