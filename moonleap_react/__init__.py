from moonleap import install
from moonleap.render.merge import add_file_merger

from . import (
    antd,
    component,
    createreactapp,
    indexfilemerger,
    module,
    nodepackage,
    prettier,
    tailwindcss,
)


def install_all():
    install(antd)
    install(component)
    install(createreactapp)
    install(module)
    install(nodepackage)
    install(prettier)
    install(tailwindcss)

    add_file_merger(indexfilemerger.IndexFileMerger())
