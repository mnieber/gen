from . import (
    authmodule,
    component,
    jsfilemerger,
    module,
    module_and_component,
    nodepackage,
    prettier,
    reactapp,
    router,
    router_and_module,
    tailwindcss,
    uikit,
    utilsmodule,
)

modules = [
    authmodule,
    component,
    module_and_component,
    module,
    nodepackage,
    prettier,
    reactapp,
    router_and_module,
    router,
    tailwindcss,
    uikit,
    utilsmodule,
]

file_mergers = [jsfilemerger.JsFileMerger()]
