from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, add, create, empty_rule, extend, kebab_to_camel, rule
from moonleap.verbs import has
from titan.react_pkg.nodepackage import load_node_package_config
from titan.react_pkg.reactapp import ReactApp, ReactAppConfig

from . import props
from .resources import ApiModule  # noqa


@create("api:module")
def create_api_module(term):
    module = ApiModule(name=kebab_to_camel(term.data))
    module.output_path = f"src/{module.name}"
    module.add_template_dir(Path(__file__).parent / "templates")
    add(module, load_node_package_config(__file__))
    add(
        module,
        ReactAppConfig(flags=dict(logQueries=False, logResourceView=False)),
    )
    return module


@rule("react-app", has, "api:module")
def react_app_has_api_module(react_app, api_module):
    react_app.utils_module.use_packages(["graphqlClient", "RST"])


rules = [(("api:module", has, "graphql:api"), empty_rule())]


@extend(ApiModule)
class ExtendApiModule:
    render = MemFun(props.render)
    graphql_api = P.child(has, "graphql:api")


@extend(ReactApp)
class ExtendReactApp:
    api_module = P.child(has, "api:module")
