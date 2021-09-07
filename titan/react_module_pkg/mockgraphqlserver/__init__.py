from pathlib import Path

import moonleap.resource.props as P
from moonleap import add, create, extend, rule
from moonleap.verbs import contains, uses
from titan.project_pkg.service import Service, Tool
from titan.react_pkg.reactapp import ReactAppConfig

from . import docker_compose_configs, dodo_layer_configs
from .props import get_context


class MockGraphqlServer(Tool):
    pass


@create("mock-graphql-server", ["tool"])
def create_mock_server(term, block):
    mock_server = MockGraphqlServer(name="mock-graphql-server")
    mock_server.output_path = "mockServer"
    mock_server.add_template_dir(Path(__file__).parent / "templates", get_context)
    add(mock_server, dodo_layer_configs.get())
    add(mock_server, docker_compose_configs.get())
    return mock_server


@rule("service", uses, "mock-graphql-server")
def add_flag(service, mock_server):
    add(
        service.react_app.app_module,
        ReactAppConfig(flags={"useMockServer": True}),
    )
    add(service.project, dodo_layer_configs.get_for_project(service.name))


@rule("store", contains, "item-type")
def store_uses_item_type(store, item_type):
    if store.module.react_app.service.mock_graphql_server:
        store.add_template_dir(Path(__file__).parent / "templates_store")


@extend(Service)
class ExtendService:
    mock_graphql_server = P.child(uses, "mock-graphql-server")
