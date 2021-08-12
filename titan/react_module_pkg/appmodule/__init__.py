import moonleap.resource.props as P
from moonleap import MemFun, add, extend, kebab_to_camel, rule, tags
from moonleap.verbs import has
from titan.react_pkg.nodepackage import load_node_package_config
from titan.react_pkg.reactapp import ReactApp
from titan.react_module_pkg.flags import StoreFlags

from . import props
from .resources import AppModule  # noqa


@tags(["app:module"])
def create_app_module(term, block):
    module = AppModule(name=kebab_to_camel(term.data))
    module.add_template_dir(__file__, "templates")
    module.output_path = f"src/{module.name}"
    add(module, load_node_package_config(__file__))
    return module


@rule("react-app", has, "app:module")
def service_has_app_module(react_app, module):
    react_app.add_template_dir(__file__, "templates_service")


@extend(ReactApp)
class ExtendReactApp:
    app_module = P.child(has, "app:module")


@extend(AppModule)
class ExtendAppModule(StoreFlags):
    get_flags = MemFun(props.get_flags)
