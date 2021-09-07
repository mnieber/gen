from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    StoreOutputPaths,
    StoreTemplateDirs,
    add_src,
    add_src_inv,
    create,
    extend,
    register_add,
)
from moonleap.verbs import has
from titan.project_pkg.project import Project
from titan.project_pkg.service import Service, Tool

from . import props
from .resources import VsCodeProject, VsCodeProjectConfig


@register_add(VsCodeProjectConfig)
def add_vs_code_project_config(resource, app_module_config):
    resource.vs_code_project_configs.add(app_module_config)


class StoreVsCodeProjectConfigs:
    vs_code_project_configs = P.tree("p-has", "vs-code-project-config")


@create("vscode-project", [])
def create_vscode_project(term, block):
    vscode_project = VsCodeProject()
    vscode_project.add_template_dir(Path(__file__).parent / "templates")
    return vscode_project


rules = [
    (("service", has, "tool"), add_src("vs_code_project_configs")),
    (("project", has, "service"), add_src("vs_code_project_configs")),
    (("project", has, "vscode-project"), add_src_inv("vs_code_project_configs")),
]


@extend(VsCodeProject)
class ExtendVsCodeProject(
    StoreOutputPaths, StoreVsCodeProjectConfigs, StoreTemplateDirs
):
    project = P.parent(Project, has)
    paths = Prop(props.paths)
    get_config = MemFun(props.get_config)


@extend(Service)
class ExtendService(StoreVsCodeProjectConfigs):
    pass


@extend(Project)
class ExtendProject(StoreVsCodeProjectConfigs):
    pass


@extend(Tool)
class ExtendTool(StoreVsCodeProjectConfigs):
    pass
