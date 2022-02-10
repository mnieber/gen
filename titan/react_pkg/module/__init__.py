import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    StoreOutputPaths,
    create,
    extend,
    feeds,
    kebab_to_snake,
)
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has
from titan.react_pkg.nodepackage import StoreNodePackageConfigs
from titan.react_pkg.packages.use_packages import use_packages
from titan.react_pkg.reactapp import ReactApp

from . import props
from .resources import Module  # noqa

rules = [(("react-app", has, "module"), feeds("output_paths"))]

base_tags = [("module", ["react-module"])]


@create("module")
def create_module(term, block):
    module = Module(name=kebab_to_snake(term.data))
    module.output_path = f"src/{module.name}"
    return module


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreNodePackageConfigs, StoreOutputPaths):
    react_app = P.parent("react-app", has, required=True)
    use_packages = MemFun(use_packages)
    module_path = Prop(props.module_path)


@extend(ReactApp)
class ExtendReactApp:
    modules = P.children(has, "module")
