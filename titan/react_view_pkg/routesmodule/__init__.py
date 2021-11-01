from pathlib import Path

import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from titan.react_pkg.reactapp import ReactApp

from .props import get_context


@rule("react-app", has, "routes:module")
def react_app_has_routes_module(react_app, routes_module):
    routes_module.add_template_dir(Path(__file__).parent / "templates", get_context)


@extend(ReactApp)
class ExtendReactApp:
    routes_module = P.child(has, "routes:module")
