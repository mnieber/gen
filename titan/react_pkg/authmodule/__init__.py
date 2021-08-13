import moonleap.resource.props as P
from moonleap import create_forward, extend, rule, tags
from moonleap.verbs import has, shows
from titan.react_pkg.reactapp import ReactApp
from titan.react_view_pkg.view.resources import View


@rule("react-app", has, "auth:module")
def react_app_has_auth_module(react_app, auth_module):
    auth_module.add_template_dir(__file__, "templates")
    react_app.api_module.add_template_dir(__file__, "templates_api")
    return [create_forward(auth_module, shows, "auth-switch:view")]


@tags(["auth-switch:view"])
def create_auth_switch(term, block):
    return View(
        name=f"AuthSwitch",
        root_filename=__file__,
        templates_dir="templates_auth_switch",
    )


@extend(ReactApp)
class ExtendReactApp:
    auth_module = P.child(has, "auth:module")
