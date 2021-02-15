import moonleap.resource.props as P
from moonleap_dodo.layer import StoreLayerConfigs
from moonleap_project.project import Project
from moonleap import MemFun, StoreOutputPaths, add, extend, render_templates, rule, tags
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
    render = MemFun(render_templates(__file__))
    project = P.parent(Project, has, "vscode-project")
