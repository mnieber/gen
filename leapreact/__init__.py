from moonleap import install

from . import createreactapp, nodepackage, prettier, reacttool, router, tailwindcss


def install_all():
    install(createreactapp)
    install(nodepackage)
    install(prettier)
    install(reacttool)
    install(router)
    install(tailwindcss)
