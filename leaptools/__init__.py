from moonleap import install

from . import (
    isort,
    makefile,
    optdir,
    pipcompile,
    pipdependency,
    pytest,
    setupfile,
    tool,
)


def install_all():
    install(isort)
    install(makefile)
    install(optdir)
    install(pipcompile)
    install(pipdependency)
    install(pytest)
    install(setupfile)
    install(tool)
