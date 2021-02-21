import moonleap.resource.props as P
from moonleap import MemFun, Rel, add, extend, render_templates, rule, tags
from moonleap.verbs import contains, has, uses
from moonleap_project.service import Service
from moonleap_react_module.flags import Flags
from moonleap_tools.tool import Tool


class MockGrapqhlServer(Tool):
    pass


def _server_name(service):
    return f"{service.name}-mock-graphql-server"


@tags(["mock-graphql-server"])
def create_mock_server(term, block):
    mock_server = MockGrapqhlServer()
    mock_server.output_path = "mockServer"
    return mock_server


@rule("service", uses, "mock-graphql-server")
def add_flag(service, mock_server):
    add(service.app_module, Flags({"useMockServer": True}))
    mock_server.output_paths.add_source(service)


@rule("store", contains, "item-list")
def store_stores_itemlist(store, item_list):
    if store.module.service.mock_graphql_server:
        store.add_template_dir(__file__, "templates_store")


@extend(MockGrapqhlServer)
class ExtendMockGrapqhlServer:
    render = MemFun(render_templates(__file__))
    service = P.parent(Service, uses, "mock-graphql-server")


@extend(Service)
class ExtendService:
    mock_graphql_server = P.child(uses, "mock-graphql-server")
