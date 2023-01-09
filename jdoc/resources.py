from dataclasses import dataclass, field

from jdoc.relations import *
from jdoc.resource import *
from jdoc.scenario import *

if T.TYPE_CHECKING:
    from jdoc.blocks import Blocks
    from jdoc.packages import *


@dataclass
class ServiceRes(Resource):
    pass


@dataclass
class PipCompileRes(Resource):
    pass


@dataclass
class BackendServiceRes(ServiceRes):
    pass


class BackendServiceUsesPipCompile(Relation):
    subj: str = "backend:service"
    verb: str = "/uses"
    obj: str = ":pip-compile"

    def fake_create_actions_for_matching_rules(self, actions: "Actions"):
        actions.actions += [Action(src_rel=self, rule=RuleServiceRunsTool())]


@dataclass
class DockerComposeRes(Resource):
    pass


class DockerComposeRunsBackendService(Relation):
    subj: str = ":docker-compose"
    verb: str = "/runs"
    obj: str = "backend:service"

    def fake_create_actions_for_matching_rules(self, actions: "Actions"):
        actions.actions += [Action(src_rel=self, rule=RuleDockerComposeRunsService())]


@dataclass
class FooProjectRes(Resource):
    services: T.List[ServiceRes] = field(default_factory=list)


class FooProjectCreated(Relation):
    subj: str = "foo:project"
    verb: str = "/is-created-as"
    obj: str = "foo:project"

    def fake_create_actions_for_matching_rules(self, actions: "Actions"):
        actions.actions += [
            Action(src_rel=self, rule=RuleCreatedProject()),
        ]


class FooProjectUsesDockerCompose(Relation):
    subj: str = "foo:project"
    verb: str = "/uses"
    obj: str = ":docker-compose"

    def fake_create_actions_for_matching_rules(self, actions: "Actions"):
        actions.actions += [
            Action(src_rel=self, rule=RuleProjectUsesDockerCompose()),
        ]


foo_project_res = FooProjectRes()
docker_compose_res = DockerComposeRes()
pip_compile_res = PipCompileRes()
backend_service_res = BackendServiceRes()


def fake_look_up_res_in_competing_blocks(term: str, blocks: "Blocks"):
    return (
        foo_project_res
        if term == "foo:project"
        else docker_compose_res
        if term == ":docker-compose"
        else pip_compile_res
        if term == ":pip-compile"
        else backend_service_res
        if term == "backend:service"
        else None
    )
