import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from titan.react_pkg.reactapp import ReactApp


@rule("react-app", has, "utils:module")
def react_app_has_utils_module(react_app, utils_module):
    utils_module.add_template_dir(__file__, "templates")


@extend(ReactApp)
class ExtendReactApp:
    utils_module = P.child(has, "utils:module")
