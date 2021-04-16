from moonleap import install

from . import django, postgresservice


def install_all():
    install(django)
    install(postgresservice)
