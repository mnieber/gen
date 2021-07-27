import moonleap.resource.props as P
from moonleap import StoreOutputPaths, extend, kebab_to_camel, rule, tags
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has
from moonleap_react.nodepackage import StoreNodePackageConfigs
from moonleap_react.reactapp import ReactApp

from .resources import Module  # noqa


@tags(["module"])
def create_module(term, block):
    module = Module(name=kebab_to_camel(term.data))
    module.output_path = f"src/{module.name}"
    return module


@rule("react-app", has, "module")
def react_app_has_module(react_app, module):
    module.output_paths.add_source(react_app)


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreNodePackageConfigs, StoreOutputPaths):
    react_app = P.parent(ReactApp, has)


@extend(ReactApp)
class ExtendReactApp:
    modules = P.children(has, "module")
