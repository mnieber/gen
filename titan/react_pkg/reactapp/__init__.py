from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import Priorities, create, create_forward, extend, get_root_resource, rule
from moonleap.blocks.verbs import has, runs
from titan.project_pkg.service import Service

from .resources import ReactApp

base_tags = {"react-app": ["tool"]}


@create("react-app")
def create_react_app(term):
    react_app = ReactApp(name="react-app")
    react_app.template_dir = Path(__file__).parent / "templates"
    react_app.template_context = dict(react_app=react_app)
    return react_app


@rule("react-app", priority=Priorities.HIGH.value)
def created_react_app(react_app):
    return [
        create_forward(react_app, has, "app:module"),
        create_forward(react_app, has, "utils:module"),
        create_forward(react_app, has, "frames:module"),
    ]


@rule("react-app")
def add_react_app_features(react_app):
    if react_app.service.get_setting_or(False, ["react_app", "reportWebVitals"]):
        get_root_resource().set_flags(["app/reportWebVitals"])


@rule("service", runs, "react-app")
def service_uses_react_app(service, react_app):
    return [create_forward(service, has, ":node-package")]


@extend(Service)
class ExtendService:
    react_app = P.child(runs, "react-app")


@extend(ReactApp)
class ExtendReactApp:
    frames_module = P.child(has, "frames:module")
    use_graphql = P.child(has, ":graphql")
