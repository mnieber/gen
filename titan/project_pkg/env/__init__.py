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
def project_created(project):
    return create_forward(project, has, ":env")


@rule("project", has, ":env")
def project_has_env(project, env):
    project.renders(
        [env],
        "env",
        dict(env=env),
        [Path(__file__).parent / "templates"],
    )
