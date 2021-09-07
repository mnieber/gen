from pathlib import Path

import moonleap.resource.props as P
from moonleap import add, create, create_forward, extend, rule
from moonleap.verbs import has, shows
from titan.react_module_pkg.store import Store
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.router_and_module import RouteTable
from titan.react_view_pkg.view import View


@rule("react-app", has, "auth:module")
def react_app_has_auth_module(react_app, auth_module):
    auth_module.add_template_dir(Path(__file__).parent / "templates")
    react_app.api_module.add_template_dir(Path(__file__).parent / "templates_api")
    add(auth_module, RouteTable(name="auth", import_path="src/auth/routeTable"))
    react_app.app_module.route_tables.add_source(auth_module)
    return [
        create_forward(auth_module, shows, "auth-switch:view"),
        create_forward(auth_module, has, "auth:store"),
        create_forward(auth_module.react_app, has, "forms:module"),
    ]


@create("auth:store", ["component"])
def create_auth_store(term, block):
    return Store(name="AuthStore")


@create("auth-switch:view", ["component"])
def create_auth_switch(term, block):
    view = View(name="AuthSwitch")
    view.add_template_dir(Path(__file__).parent / "templates_auth_switch")
    return view


@extend(ReactApp)
class ExtendReactApp:
    auth_module = P.child(has, "auth:module")
