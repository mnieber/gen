import moonleap.resource.props as P
from moonleap import add, create_forward, extend, rule
from moonleap.verbs import has
from titan.react_pkg.reactapp import ReactApp
from titan.react_view_pkg.router import RouteTable


@rule("react-app", has, "auth:module")
def react_app_has_auth_module(react_app, auth_module):
    add(auth_module, RouteTable(name="auth", import_path="src/auth/routeTable"))
    return [
        create_forward(auth_module.react_app, has, "forms:module"),
    ]


@extend(ReactApp)
class ExtendReactApp:
    auth_module = P.child(has, "auth:module")
