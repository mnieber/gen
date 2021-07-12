from moonleap import install

from . import django, postgresservice, strapi, strapidockerimage


def install_all():
    install(django)
    install(postgresservice)
    install(strapi)
    install(strapidockerimage)
