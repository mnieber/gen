from moonleap import install

from . import (
    antd,
    appmodule,
    createreactapp,
    module,
    nodepackage,
    prettier,
    router,
    tailwindcss,
)


def install_all():
    install(antd)
    install(appmodule)
    install(createreactapp)
    install(module)
    install(nodepackage)
    install(prettier)
    install(router)
    install(tailwindcss)
