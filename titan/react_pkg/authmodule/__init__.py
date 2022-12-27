from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, extend, rule
from moonleap.blocks.verbs import has
from moonleap.render.render_mixin import get_root_resource
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule


@create("auth:module")
def create_module(term):
    module = ReactModule(name="auth")
    module.template_dir = Path(__file__).parent / "templates"
    return module


@rule("react-app", has, "auth:module")
def react_app_has_auth_module(react_app, auth_module):
    get_root_resource().set_flags(["utils/useNextUrl"])
    return [
        create_forward(auth_module.react_app, has, "forms:module"),
        create_forward(auth_module.react_app, has, ":graphql"),
    ]


@extend(ReactApp)
class ExtendReactApp:
    auth_module = P.child(has, "auth:module")
