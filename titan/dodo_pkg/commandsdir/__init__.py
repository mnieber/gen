from pathlib import Path

import moonleap.resource.props as P
from moonleap import add, create, extend, rule
from moonleap.verbs import has
from titan.project_pkg.project import Project

from . import dodo_layer_configs
from .resources import CommandsDir


@create("commands-dir", [])
def create_commands_dir(term, block):
    commands_dir = CommandsDir(name=term.data)
    return commands_dir


@rule("project", has, "commands-dir")
def project_has_commands_dir(project, commands_dir):
    project.add_template_dir(Path(__file__).parent / "templates_project")
    add(project, dodo_layer_configs.get(project))


@extend(Project)
class ExtendProject:
    commands_dir = P.child(has, "commands-dir")
