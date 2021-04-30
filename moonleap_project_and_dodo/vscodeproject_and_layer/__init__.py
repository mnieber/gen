from moonleap import add, extend, rule
from moonleap.verbs import has
from moonleap_dodo.layer import StoreLayerConfigs
from moonleap_project.vscodeproject.resources import VsCodeProject

from . import layer_configs


@rule("project", has, "vscode-project")
def project_has_vscode_project(project, vscode_project):
    add(project, layer_configs.get(project))


@extend(VsCodeProject)
class ExtendVsCodeProject(StoreLayerConfigs):
    pass
