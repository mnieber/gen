from moonleap import install

from . import (
    createreactapp,
    django,
    fish,
    isort,
    makefile,
    nodepackage,
    optdir,
    pipcompile,
    pipdependency,
    pudb,
    pytest,
    pythondockerimage,
    setupfile,
    tool,
)


def install_all():
    install(createreactapp)
    install(django)
    install(fish)
    install(isort)
    install(makefile)
    install(optdir)
    install(nodepackage)
    install(pipcompile)
    install(pipdependency)
    install(pudb)
    install(pytest)
    install(pythondockerimage)
    install(setupfile)
    install(tool)
