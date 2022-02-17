from pathlib import Path

import moonleap.resource.props as P
from moonleap import add, create, create_forward, extend, receives, rule
from moonleap.verbs import has, shows
from titan.react_pkg.reactapp import ReactApp
from titan.react_view_pkg.router_and_module import RouteTable

from .resources import AuthStore, AuthSwitchView


@rule("react-app", has, "auth:module")
def react_app_has_auth_module(react_app, auth_module):
    auth_module.add_template_dir(Path(__file__).parent / "templates")
    react_app.api_module.add_template_dir(Path(__file__).parent / "templates_api")
    add(auth_module, RouteTable(name="auth", import_path="src/auth/routeTable"))
    receives("route_tables")(react_app.app_module, auth_module)
    return [
        create_forward(auth_module, has, "auth-switch:view"),
        create_forward(auth_module, shows, "+auth-switch:view"),
        create_forward(auth_module, has, "auth:store"),
        create_forward(auth_module.react_app, has, "forms:module"),
    ]


@create("auth:store")
def create_auth_store(term):
    return AuthStore(name="AuthStore")


@rule("module", has, "auth:store")
def module_has_store(module, auth_store):
    pass


@create("auth-switch:view")
def create_auth_switch(term):
    view = AuthSwitchView(name="AuthSwitch")
    view.add_template_dir(Path(__file__).parent / "templates_auth_switch")
    return view


@extend(ReactApp)
class ExtendReactApp:
    auth_module = P.child(has, "auth:module")
