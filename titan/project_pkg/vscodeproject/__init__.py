import moonleap.extension.props as P
from moonleap import create, empty_rule, extend
from moonleap.spec.verbs import has
from titan.project_pkg.project import Project

from .resources import VsCodeProject


@create("vscode-project")
def create_vscode_project(term):
    return VsCodeProject()


@extend(Project)
class ExtendProject:
    vscode_project = P.child(has, "vscode-project")


@extend(VsCodeProject)
class ExtendVsCodeProject:
    project = P.parent("project", has)


rules = {"project": {(has, "vscode-project"): empty_rule()}}
