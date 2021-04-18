from moonleap import install

from . import (
    appmodule,
    appstore,
    dataloader,
    flags,
    graphqlapi,
    graphqlapi_and_dataloader,
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
    install(dataloader)
    install(flags)
    install(graphqlapi)
    install(graphqlapi_and_dataloader)
    install(item)
    install(itemlist)
    install(itemtype)
    install(store)
    install(storeprovider)
    install(utilsmodule)
