from moonleap import install

from . import (
    django,
    fish,
    isort,
    makefile,
    nodedockerimage,
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
    install(django)
    install(fish)
    install(isort)
    install(makefile)
    install(nodedockerimage)
    install(optdir)
    install(pipcompile)
    install(pipdependency)
    install(pudb)
    install(pytest)
    install(pythondockerimage)
    install(setupfile)
    install(tool)
