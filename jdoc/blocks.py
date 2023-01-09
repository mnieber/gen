from dataclasses import dataclass, field

from jdoc.packages import *
from jdoc.resources import *
from jdoc.scenario import *
from jdoc.settings import *
from jdoc.verbs import *


@dataclass
class Line(Entity):
    terms: T.List[str] = field(default_factory=list)


@dataclass
class Block(Entity):
    name: str = ""
    lines: list[Line] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)
    scopes: list[Scope] = field(default_factory=list)


@dataclass
class MainBlock(Block):
    foo_project_uses_docker_compose: FooProjectUsesDockerCompose = field(init=False)
    docker_compose_runs_backend_service: DockerComposeRunsBackendService = field(
        init=False
    )

    def fake_get_lines_from_expanded_markdown(self, expanded_markdown):
        self.name = "The foo:project"
        self.lines = [
            Line(terms=["foo:project"]),
            Line(
                terms=[
                    "foo:project",
                    "/uses",
                    ":docker-compose",
                    "/runs",
                    "backend:service",
                ]
            ),
        ]

    def fake_get_scopes_from_settings(self):
        self.scopes = [global_settings.scope_by_name["default"]]

    def fake_get_relations(self):
        self.foo_project_uses_docker_compose = FooProjectUsesDockerCompose()
        self.docker_compose_runs_backend_service = DockerComposeRunsBackendService()
        self.relations = [
            self.foo_project_uses_docker_compose,
            self.docker_compose_runs_backend_service,
        ]


@dataclass
class BackendServiceBlock(Block):
    backend_service_uses_pip_compile: BackendServiceUsesPipCompile = field(init=False)

    def fake_get_lines_from_expanded_markdown(self, expanded_markdown):
        self.name = "The backend:service"
        self.lines = [
            Line(terms=["backend:service"]),
            Line(terms=["backend:service", "/uses", ":pip-compile"]),
        ]

    def fake_get_scopes_from_settings(self):
        self.scopes = [
            global_settings.scope_by_name["default"],
            global_settings.scope_by_name["backend-service"],
        ]

    def fake_get_relations(self):
        self.backend_service_uses_pip_compile = BackendServiceUsesPipCompile()
        self.relations = [self.backend_service_uses_pip_compile]


@dataclass
class Blocks(Entity):
    main_block: MainBlock = field(init=False)
    backend_service_block: BackendServiceBlock = field(init=False)
    actions: Actions = field(init=False)
