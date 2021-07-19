from moonleap import install
from moonleap.render.merge import add_file_merger

from . import (
    component,
    createreactapp,
    jsfilemerger,
    module,
    module_and_component,
    nodepackage,
    prettier,
    tailwindcss,
    uikit,
)


def install_all():
    install(component)
    install(createreactapp)
    install(module)
    install(module_and_component)
    install(nodepackage)
    install(prettier)
    install(tailwindcss)
    install(uikit)

    add_file_merger(jsfilemerger.JsFileMerger())
