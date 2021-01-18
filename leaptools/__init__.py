from moonleap import install

from . import (
    createreactapp,
    isort,
    makefile,
    nodepackage,
    optdir,
    pipcompile,
    pipdependency,
    pytest,
    setupfile,
    tool,
)


def install_all():
    install(createreactapp)
    install(isort)
    install(makefile)
    install(optdir)
    install(nodepackage)
    install(pipcompile)
    install(pipdependency)
    install(pytest)
    install(setupfile)
    install(tool)
