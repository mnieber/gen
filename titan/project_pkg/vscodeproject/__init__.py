import moonleap.resource.props as P
from moonleap import RenderTemplates, StoreOutputPaths, extend, create
from moonleap.verbs import has
from titan.project_pkg.project import Project

from .resources import VsCodeProject


@create(["vscode-project"])
def create_vscode_project(term, block):
    vscode_project = VsCodeProject()
    return vscode_project


@extend(VsCodeProject)
class ExtendVsCodeProject(StoreOutputPaths, RenderTemplates(__file__)):
    project = P.parent(Project, has)
