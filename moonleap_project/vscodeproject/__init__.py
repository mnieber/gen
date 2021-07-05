import moonleap.resource.props as P
from moonleap import MemFun, StoreOutputPaths, extend, render_templates, tags
from moonleap.verbs import has
from moonleap_project.project import Project

from .resources import VsCodeProject


@tags(["vscode-project"])
def create_vscode_project(term, block):
    vscode_project = VsCodeProject()
    return vscode_project


@extend(VsCodeProject)
class ExtendVsCodeProject(StoreOutputPaths):
    render = MemFun(render_templates(__file__))
    project = P.parent(Project, has)
