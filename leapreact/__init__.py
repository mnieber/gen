from moonleap import install

from . import (
    appmodule,
    createreactapp,
    module,
    nodepackage,
    prettier,
    reacttool,
    router,
    tailwindcss,
)


def install_all():
    install(appmodule)
    install(createreactapp)
    install(module)
    install(nodepackage)
    install(prettier)
    install(reacttool)
    install(router)
    install(tailwindcss)
