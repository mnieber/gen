import moonleap.resource.props as P
from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import contains, uses
from titan.project_pkg.service import Service, Tool
from titan.react_module_pkg.flags import Flags

from . import docker_compose_configs, layer_configs, props


class MockGrapqhlServer(Tool):
    pass


@tags(["mock-graphql-server"])
def create_mock_server(term, block):
    mock_server = MockGrapqhlServer(name="mock-graphql-server")
    mock_server.output_path = "mockServer"
    add(mock_server, layer_configs.get())
    add(mock_server, docker_compose_configs.get())
    return mock_server


@rule("service", uses, "mock-graphql-server")
def add_flag(service, mock_server):
    add(service.react_app.app_module, Flags({"useMockServer": True}))
    add(service.project, layer_configs.get_for_project(service.name))


@rule("store", contains, "item-type")
def store_uses_item_type(store, item_type):
    if store.module.react_app.service.mock_graphql_server:
        store.add_template_dir(__file__, "templates_store")


@extend(MockGrapqhlServer)
class ExtendMockGrapqhlServer:
    render = MemFun(render_templates(__file__))
    service = P.parent(Service, uses)
    p_section_item_fields = MemFun(props.p_section_item_fields)


@extend(Service)
class ExtendService:
    mock_graphql_server = P.child(uses, "mock-graphql-server")
