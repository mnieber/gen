import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from titan.react_pkg.reactapp import ReactApp


@rule("react-app", has, "auth:module")
def react_app_has_auth_module(react_app, auth_module):
    auth_module.add_template_dir(__file__, "templates")


@extend(ReactApp)
class ExtendReactApp:
    auth_module = P.child(has, "auth:module")
