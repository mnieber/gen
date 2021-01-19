import moonleap.resource.props as P
from leapproject.dockercompose import DockerComposeConfig
from leapproject.service import Service
from moonleap import MemFun, extend, rule, tags
from moonleap.verbs import has

from . import docker_compose_configs as DCC
from . import props
from .resources import OptDir, OptPath  # noqa


@tags(["opt-dir"])
def create_opt_dir(term, block):
    opt_dir = OptDir()
    return opt_dir


@rule("service", has, "opt-dir")
def service_has_opt_dir(service, opt_dir):
    service.docker_compose_configs.add(
        DockerComposeConfig(lambda x: DCC.get(opt_dir), is_dev=True)
    )


class StoreOptPaths:
    opt_paths = P.tree(has, "opt-path")


@extend(OptDir)
class ExtendOptDir:
    render = MemFun(props.render_opt_dir)
    service = P.parent(Service, has, "opt-dir")
