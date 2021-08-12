import moonleap.resource.props as P
from moonleap import add, create_forward, extend, rule, tags
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has, runs
from titan.project_pkg.service import Service, Tool
from titan.react_pkg.nodepackage import load_node_package_config

from . import docker_compose_configs, layer_configs, makefile_rules


class ReactApp(Tool):
    pass


@tags(["react-app"])
def create_react_app(term, block):
    react_app = ReactApp(name="react-app")
    react_app.add_template_dir(__file__, "templates")
    add(react_app, load_node_package_config(__file__))
    add(react_app, docker_compose_configs.get(is_dev=True))
    add(react_app, docker_compose_configs.get(is_dev=False))
    add(react_app, makefile_rules.get())
    return react_app


@rule("react-app")
def create_react_created(react_app):
    return [
        create_forward(react_app, has, "app:module"),
        create_forward(react_app, has, "utils:module"),
    ]


@rule("service", runs, "react-app")
def service_uses_react_app(service, react_app):
    service.port = service.port or "3000"
    add(service.project, layer_configs.get_for_project(service.name))
    return [
        create_forward(service, has, ":makefile"),
        create_forward(service, has, ":node-package"),
    ]


@extend(ReactApp)
class ExtendReactApp(StoreTemplateDirs):
    service = P.parent(Service, runs)


@extend(Service)
class ExtendService:
    react_app = P.child(runs, "react-app")
