from dataclasses import dataclass
from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import RenderMixin, Resource, create, extend, rule
from moonleap.blocks.verbs import has
from titan.project_pkg.project import Project


@dataclass
class CommandsDir(RenderMixin, Resource):
    pass


@create("commands-dir")
def create_commands_dir(term):
    return CommandsDir()


@rule("project", has, "commands-dir")
def project_has_commands_dir(project, commands_dir):
    project.renders(
        #
        [commands_dir],
        "",
        dict(),
        [Path(__file__).parent / "templates"],
    )


@extend(Project)
class ExtendProject:
    commands_dir = P.child(has, "commands-dir")
