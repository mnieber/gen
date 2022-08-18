from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, empty_rule, extend, get_root_resource, rule
from moonleap.verbs import has
from titan.project_pkg.project import Project

from .resources import VsCodeProject

rules = [(("project", has, "vscode-project"), empty_rule())]


@create("vscode-project")
def create_vscode_project(term):
    return VsCodeProject()


@rule("vscode-project")
def created_vscode_project(vscode_project):
    get_root_resource().renders(
        [vscode_project],
        "",
        dict(vscode_project=vscode_project),
        [Path(__file__).parent / "templates"],
    )


@extend(Project)
class ExtendProject:
    vscode_project = P.child(has, "vscode-project")


@extend(VsCodeProject)
class ExtendVsCodeProject:
    project = P.parent("project", has)
