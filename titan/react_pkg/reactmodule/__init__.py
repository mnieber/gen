import moonleap.resource.props as P
from moonleap import MemFun, Prop, create, empty_rule, extend, kebab_to_camel, rule
from moonleap.verbs import has
from titan.react_pkg.packages.use_packages import use_packages
from titan.react_pkg.reactapp import ReactApp

from . import props
from .resources import ReactModule  # noqa

rules = [
    (("react-app", has, "module"), empty_rule()),
]


base_tags = [("module", ["react-module"])]


@create("module")
def create_module(term):
    module = ReactModule(name=kebab_to_camel(term.data))
    return module


@rule("react-app", has, "module")
def react_app_has_module(react_app, module):
    react_app.renders(
        module,
        f"src/{module.name}",
        module.template_context,
        [module.template_dir],
    )


@extend(ReactModule)
class ExtendModule:
    react_app = P.parent("react-app", has, required=True)
    use_packages = MemFun(use_packages)
    module_path = Prop(props.module_path)


@extend(ReactApp)
class ExtendReactApp:
    modules = P.children(has, "module")
    get_module = MemFun(props.get_module)
