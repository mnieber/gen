from dataclasses import dataclass
from pathlib import Path

from moonleap import create, create_forward, rule
from moonleap.blocks.verbs import has
from titan.project_pkg.service import Tool


@dataclass
class Env(Tool):
    pass


@create("env")
def create_env(term):
    env = Env("env")
    env.template_dir = Path(__file__).parent / "templates"
    env.template_context = dict(env=env)
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
    },
}
