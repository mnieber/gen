import moonleap.resource.props as P
from leapdodo.layer import StoreLayerConfigs
from leapproject.project import Project
from moonleap import StoreOutputPaths, add, extend, render_templates, rule, tags
from moonleap.verbs import has

from . import layer_configs
from .resources import VsCodeProject


@tags(["vscode-project"])
def create_vscode_project(term, block):
    vscode_project = VsCodeProject()
    return vscode_project


@rule("project", has, "vscode-project")
def project_has_vscode_project(project, vscode_project):
    add(project, layer_configs.get(project))


@extend(VsCodeProject)
class ExtendVsCodeProject(StoreOutputPaths, StoreLayerConfigs):
    render = render_templates(__file__)
    project = P.parent(Project, has, "vscode-project")
