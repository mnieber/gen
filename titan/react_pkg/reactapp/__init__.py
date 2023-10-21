from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import Priorities, create, create_forward, empty_rule, extend, rule
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
        create_forward(react_app, has, ":node-package"),
    ]


@extend(Service)
class ExtendService:
    react_app = P.child(runs, "react-app")


@extend(ReactApp)
class ExtendReactApp:
    frames_module = P.child(has, "frames:module")
    use_graphql = P.child(has, ":graphql")
    node_package = P.child(has, "node-package")


rules = {
    "react-app": {(has, "node-package"): empty_rule()},
}
