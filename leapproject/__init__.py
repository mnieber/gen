from moonleap import install

from . import (
    configlayer,
    dockercompose,
    dockerfile,
    project,
    service,
    servicelayergroup,
    srcdir,
    vscodeproject,
)


def install_all():
    install(configlayer)
    install(dockercompose)
    install(dockerfile)
    install(project)
    install(service)
    install(servicelayergroup)
    install(srcdir)
    install(vscodeproject)
