from moonleap import install

from . import (
    configlayer,
    dockercompose,
    dockerfile,
    makefile,
    optdir,
    pipcompile,
    pipdependency,
    project,
    pytest,
    service,
    servicelayergroup,
    srcdir,
    tool,
)


def install_all():
    install(configlayer)
    install(dockercompose)
    install(dockerfile)
    install(makefile)
    install(optdir)
    install(pipcompile)
    install(pipdependency)
    install(project)
    install(pytest)
    install(service)
    install(servicelayergroup)
    install(srcdir)
    install(tool)
