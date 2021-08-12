from moonleap import add, extend, rule
from moonleap.verbs import has
from titan.dodo_pkg.layer import StoreLayerConfigs
from titan.project_pkg.vscodeproject.resources import VsCodeProject

from . import layer_configs


@rule("project", has, "vscode-project")
def project_has_vscode_project(project, vscode_project):
    add(project, layer_configs.get(project))


@extend(VsCodeProject)
class ExtendVsCodeProject(StoreLayerConfigs):
    pass
