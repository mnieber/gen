from moonleap import install

from . import django, postgresservice, strapidockerimage


def install_all():
    install(django)
    install(postgresservice)
    install(strapidockerimage)
