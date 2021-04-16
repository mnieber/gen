from moonleap import install

from . import (
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
    tool_extensions,
    vandelay,
)


def install_all():
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
    install(tool_extensions)
    install(vandelay)
