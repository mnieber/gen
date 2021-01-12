from moonleap.install import install

from . import (
    configlayer,
    dockercompose,
    dockerfile,
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
    tool,
)


def install_all():
    install(configlayer)
    install(dockercompose)
    install(dockerfile)
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
    install(tool)
