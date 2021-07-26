import moonleap.resource.props as P
from moonleap import MemFun, add, extend, register_add, rule, tags
from moonleap.verbs import has
from moonleap_project.service import Service, Tool

from . import docker_compose_configs, props
from .resources import OptDir, OptPath  # noqa


@tags(["opt-dir"])
def create_opt_dir(term, block):
    opt_dir = OptDir()
    return opt_dir


@rule("service", has, "opt-dir")
def service_has_opt_dir(service, opt_dir):
    add(service, docker_compose_configs.get(opt_dir))


@register_add(OptPath)
def add_optpath(resource, opt_path):
    resource.opt_paths.add(opt_path)


class StoreOptPaths:
    opt_paths = P.tree(has, "opt-path")


@extend(OptDir)
class ExtendOptDir:
    render = MemFun(props.render_opt_dir)
    service = P.parent(Service, has)


@extend(Service)
class ExtendService:
    opt_dir = P.child(has, "opt-dir")


@extend(Tool)
class ExtendTool(StoreOptPaths):
    pass
