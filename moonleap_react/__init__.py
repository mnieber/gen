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

modules = [
    (component),
    (createreactapp),
    (module),
    (module_and_component),
    (nodepackage),
    (prettier),
    (tailwindcss),
    (uikit),
]

file_mergers = [jsfilemerger.JsFileMerger()]
