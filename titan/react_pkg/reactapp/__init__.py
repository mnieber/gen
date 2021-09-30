from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Priorities,
    add,
    create,
    create_forward,
    extend,
    register_add,
    rule,
)
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has
from titan.react_pkg.nodepackage import load_node_package_config
from titan.react_pkg.packages.use_packages import use_packages

from . import docker_compose_configs, makefile_rules, props, react_app_configs
from .props import get_context
from .resources import ReactApp, ReactAppConfig


@register_add(ReactAppConfig)
def add_react_app_config(resource, app_module_config):
    resource.react_app_configs.add(app_module_config)


class StoreReactAppConfigs:
    react_app_configs = P.tree("p-has", "react-app-config")


base_tags = [("react-app", ["tool"])]


@create("react-app")
def create_react_app(term, block):
    react_app = ReactApp(name="react-app")
    react_app.add_template_dir(Path(__file__).parent / "templates", get_context)
    add(react_app, load_node_package_config(__file__))
    add(react_app, docker_compose_configs.get(is_dev=True))
    add(react_app, docker_compose_configs.get(is_dev=False))
    add(react_app, makefile_rules.get_runserver())
    add(react_app, makefile_rules.get_install())
    return react_app


@rule("react-app", priority=Priorities.HIGH.value)
def create_react_created(react_app):
    return [
        create_forward(react_app, has, "app:module"),
        create_forward(react_app, has, "utils:module"),
    ]


@rule("react-app")
def use_webvitals(react_app):
    if react_app.service.get_tweak_or(True, ["react_app", "reportWebVitals"]):
        add(react_app, react_app_configs.get())
        react_app.use_packages(["reportWebVitals"])


@extend(ReactApp)
class ExtendReactApp(StoreTemplateDirs, StoreReactAppConfigs):
    use_packages = MemFun(use_packages)
    get_flags = MemFun(props.get_flags)
