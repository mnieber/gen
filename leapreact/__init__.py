from moonleap import install

from . import (
    antd,
    appmodule,
    component,
    createreactapp,
    module,
    nodepackage,
    prettier,
    router,
    store,
    storeprovider,
    tailwindcss,
)


def install_all():
    install(antd)
    install(appmodule)
    install(component)
    install(createreactapp)
    install(module)
    install(nodepackage)
    install(prettier)
    install(router)
    install(store)
    install(storeprovider)
    install(tailwindcss)
