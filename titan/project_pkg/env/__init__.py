from dataclasses import dataclass

from moonleap import create, create_forward, empty_rule, rule
from moonleap.blocks.verbs import has
from titan.project_pkg.service import Tool


@dataclass
class Env(Tool):
    pass


@create("env")
def create_env(term):
    env = Env("env")
    return env


@rule("project")
def created_project(project):
    return create_forward(project, has, ":env")


def project_has_service_that_has_env(project, service):
    if service.has_env:
        return create_forward(service, has, ":env")


rules = {
    "project": {
        (has, "service"): (
            # then maybe create relation :service /has :env
            project_has_service_that_has_env
        ),
        (has, ":env"): empty_rule(),
    },
    "service": {
        (has, ":env"): empty_rule(),
    },
}
