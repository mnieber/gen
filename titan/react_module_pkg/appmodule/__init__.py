import moonleap.resource.props as P
from moonleap import add, extend, kebab_to_camel, rule, tags
from moonleap.verbs import has
from titan.react_pkg.nodepackage import load_node_package_config
from titan.react_pkg.reactapp import ReactApp

from .resources import AppModule  # noqa


@tags(["app:module"])
def create_app_module(term, block):
    module = AppModule(name=kebab_to_camel(term.data))
    module.add_template_dir(__file__, "templates")
    module.output_path = f"src/{module.name}"
    module.use_packages(["reportWebVitals"])
    add(module, load_node_package_config(__file__))
    return module


@extend(ReactApp)
class ExtendReactApp:
    app_module = P.child(has, "app:module")
