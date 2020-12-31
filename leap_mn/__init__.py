from moonleap.config import config, install
from ramda import merge

from . import (
    dockercompose,
    dockerfile,
    gitrepository,
    layer,
    layergroup,
    makefile,
    pipcompile,
    pipdependency,
    project,
    pytest,
    pytesthtml,
    service,
    srcdir,
)


def install_all():
    install(dockercompose)
    install(dockerfile)
    install(gitrepository)
    install(layer)
    install(layergroup)
    install(makefile)
    install(pipcompile)
    install(pipdependency)
    install(project)
    install(pytest)
    install(pytesthtml)
    install(service)
    install(srcdir)
