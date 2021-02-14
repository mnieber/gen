from moonleap import install

from . import (
    antd,
    appmodule,
    appstore,
    component,
    createreactapp,
    graphqlapi,
    itemlist,
    module,
    nodepackage,
    prettier,
    router,
    store,
    storeprovider,
    tailwindcss,
    utilsmodule,
)


def install_all():
    install(antd)
    install(appmodule)
    install(appstore)
    install(component)
    install(createreactapp)
    install(graphqlapi)
    install(itemlist)
    install(module)
    install(nodepackage)
    install(prettier)
    install(router)
    install(store)
    install(storeprovider)
    install(tailwindcss)
    install(utilsmodule)
