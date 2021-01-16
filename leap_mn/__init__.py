from moonleap import install

from . import (
    configlayer,
    dockercompose,
    dockerfile,
    isort,
    makefile,
    optdir,
    pipcompile,
    pipdependency,
    project,
    pytest,
    service,
    servicelayergroup,
    setupfile,
    srcdir,
    tool,
)


def install_all():
    install(configlayer)
    install(dockercompose)
    install(dockerfile)
    install(isort)
    install(makefile)
    install(optdir)
    install(pipcompile)
    install(pipdependency)
    install(project)
    install(pytest)
    install(setupfile)
    install(service)
    install(servicelayergroup)
    install(srcdir)
    install(tool)
