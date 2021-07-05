import moonleap.resource.props as P
from moonleap import MemFun, add, create_forward, extend, render_templates, rule, tags
from moonleap.verbs import has, uses
from moonleap_react.nodepackage import load_node_package_config
from moonleap_tools.tool import Tool

from . import docker_compose_configs, layer_configs


class CreateReactApp(Tool):
    pass


@tags(["create-react-app"])
def create_cra(term, block):
    cra = CreateReactApp()
    add(cra, load_node_package_config(__file__))
    add(cra, docker_compose_configs.get(is_dev=True))
    add(cra, docker_compose_configs.get(is_dev=False))
    return cra


@rule("service", uses, "create-react-app")
def service_uses_cra(service, cra):
    service.port = service.port or "3000"
    add(service.project, layer_configs.get_for_project(service.name))
    return [
        create_forward(service, has, "app:module"),
        create_forward(service, has, "utils:module"),
    ]


def meta():
    from moonleap_project.service import Service

    @extend(CreateReactApp)
    class ExtendCreateReactApp:
        render = MemFun(render_templates(__file__))

    @extend(Service)
    class ExtendService:
        cra = P.child(has, "create-react-app")

    return [ExtendCreateReactApp, ExtendService]
