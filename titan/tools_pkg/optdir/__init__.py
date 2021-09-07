import moonleap.resource.props as P
from moonleap import MemFun, add, create, extend, register_add
from moonleap.verbs import has
from titan.project_pkg.service import Service, Tool

from . import docker_compose_configs, props
from .resources import OptDir, OptPath  # noqa


@create("opt-dir", ["tool"])
def create_opt_dir(term, block):
    opt_dir = OptDir(name="opt-dir")
    add(opt_dir, docker_compose_configs.get(opt_dir))
    return opt_dir


@register_add(OptPath)
def add_optpath(resource, opt_path):
    resource.opt_paths.add(opt_path)


class StoreOptPaths:
    opt_paths = P.tree("p-has", "opt-path")


@extend(OptDir)
class ExtendOptDir:
    render = MemFun(props.render_opt_dir)


@extend(Service)
class ExtendService:
    opt_dir = P.child(has, "opt-dir")


@extend(Tool)
class ExtendTool(StoreOptPaths):
    pass
