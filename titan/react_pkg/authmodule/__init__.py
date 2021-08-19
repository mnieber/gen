import moonleap.resource.props as P
from moonleap import add, create_forward, extend, rule, tags
from moonleap.verbs import has, shows
from titan.react_module_pkg.store import Store
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.router_and_module import RouteTable
from titan.react_view_pkg.view import View


@rule("react-app", has, "auth:module")
def react_app_has_auth_module(react_app, auth_module):
    auth_module.add_template_dir(__file__, "templates")
    react_app.api_module.add_template_dir(__file__, "templates_api")
    add(auth_module, RouteTable(name="auth", import_path="src/auth/routeTable"))
    react_app.app_module.route_tables.add_source(auth_module)
    return [
        create_forward(auth_module, shows, "auth-switch:view"),
        create_forward(auth_module, has, "auth:store"),
        create_forward(auth_module.react_app, has, "forms:module"),
    ]


@tags(["auth:store"])
def create_auth_store(term, block):
    return Store(name="AuthStore")


@tags(["auth-switch:view"])
def create_auth_switch(term, block):
    return View(
        name="AuthSwitch",
        root_filename=__file__,
        templates_dir="templates_auth_switch",
    )


@extend(ReactApp)
class ExtendReactApp:
    auth_module = P.child(has, "auth:module")
