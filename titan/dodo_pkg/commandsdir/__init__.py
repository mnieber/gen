from dataclasses import dataclass

import moonleap.packages.extensions.props as P
from moonleap import Resource, create, extend
from moonleap.blocks.verbs import has
from titan.project_pkg.project import Project


@dataclass
class CommandsDir(Resource):
    pass


@create("commands-dir")
def create_commands_dir(term):
    return CommandsDir()


@extend(Project)
class ExtendProject:
    commands_dir = P.child(has, "commands-dir")
