from dataclasses import dataclass
from pathlib import Path

from moonleap import create, create_forward, empty_rule, rule
from moonleap.verbs import has
from titan.project_pkg.service import Tool

rules = {
    ("project", has, "env"): empty_rule(),
}


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


@rule("project", has, "service")
def project_has_service_that_has_env(project, service):
    return create_forward(service, has, ":env")


@rule("project", has, ":env")
def project_has_env(project, env):
    project.renders(
        [env],
        "env",
        dict(env=env),
        [Path(__file__).parent / "templates"],
    )


@rule("service", has, ":env")
def service_has_env(service, env):
    service.renders(
        [env],
        ".env",
        dict(env=env),
        [Path(__file__).parent / "templates_service"],
    )
