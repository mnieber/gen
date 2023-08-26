from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, extend, rule
from moonleap.blocks.verbs import has
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule, create_react_module


@create("auth:module")
def create_auth_module(term):
    return create_react_module(ReactModule, term, Path(__file__).parent / "templates")


@rule("react-app", has, "auth:module")
def react_app_has_auth_module(react_app, auth_module):
    react_app.set_flags(["utils/useNextUrl"])
    return [
        create_forward(auth_module.react_app, has, "forms:module"),
        create_forward(auth_module.react_app, has, ":graphql"),
    ]


@extend(ReactApp)
class ExtendReactApp:
    auth_module = P.child(has, "auth:module")
