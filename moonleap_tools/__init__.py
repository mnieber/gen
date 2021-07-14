from moonleap import install

from . import (
    black,
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
    install(black)
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
    install(tool_extensions)
    install(tool)
    install(vandelay)
