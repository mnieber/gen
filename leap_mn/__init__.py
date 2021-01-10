from moonleap.install import install

from . import (
    dockercompose,
    dockerfile,
    dodoconfig,
    gitrepository,
    layer,
    layerconfig,
    layergroup,
    makefile,
    pipcompile,
    pipdependency,
    project,
    pytest,
    pytesthtml,
    service,
    servicelayergroup,
    srcdir,
)


def install_all():
    install(dockercompose)
    install(dockerfile)
    install(dodoconfig)
    install(gitrepository)
    install(layer)
    install(layerconfig)
    install(layergroup)
    install(makefile)
    install(pipcompile)
    install(pipdependency)
    install(project)
    install(pytest)
    install(pytesthtml)
    install(service)
    install(servicelayergroup)
    install(srcdir)
