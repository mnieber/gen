from moonleap import install

from . import (
    antd,
    component,
    createreactapp,
    module,
    nodepackage,
    prettier,
    tailwindcss,
)


def install_all():
    install(antd)
    install(component)
    install(createreactapp)
    install(module)
    install(nodepackage)
    install(prettier)
    install(tailwindcss)
