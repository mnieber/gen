from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, extend, rule
from moonleap.blocks.verbs import has
from titan.react_pkg.packages.use_react_package import use_react_package
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule


@create("auth:module")
def create_module(term):
    module = ReactModule(name="auth")
    module.template_dir = Path(__file__).parent / "templates"
    return module


@rule("react-app", has, "auth:module")
def react_app_has_auth_module(react_app, auth_module):
    use_react_package(react_app.get_module("utils"), "hooks/useNextUrl", "hooks")
    return [
        create_forward(auth_module.react_app, has, "forms:module"),
        create_forward(auth_module.react_app, has, ":graphql"),
    ]


@extend(ReactApp)
class ExtendReactApp:
    auth_module = P.child(has, "auth:module")
