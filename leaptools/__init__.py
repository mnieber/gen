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
    prettier,
    pudb,
    pytest,
    pythondockerimage,
    setupfile,
    tailwindcss,
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
    install(prettier)
    install(pudb)
    install(pytest)
    install(pythondockerimage)
    install(setupfile)
    install(tailwindcss)
    install(tool)
