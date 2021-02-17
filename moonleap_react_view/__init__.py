from moonleap import install

from . import listview, router


def install_all():
    install(listview)
    install(router)
