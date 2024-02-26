
import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, extend
from moonleap.blocks.verbs import has
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import create_react_module

from .resources import AuthModule


@create("auth:module")
def create_auth_module(term):
    return create_react_module(AuthModule, term)


@extend(ReactApp)
class ExtendReactApp:
    auth_module = P.child(has, "auth:module")


rules = {
    "react-app": {
        (has, "auth:module"): (
            # then react_app has a forms module and graphql
            lambda react_app, auth_module: [
                create_forward(react_app, has, "forms:module"),
                create_forward(react_app, has, ":graphql"),
            ]
        )
    }
}
