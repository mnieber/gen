import moonleap.resource.props as P
from leap_mn.dockercompose import DockerComposeConfig
from leap_mn.service import Service
from moonleap import MemFun, extend, rule, tags

from . import props
from .resources import OptDir, OptPath  # noqa


@tags(["opt-dir"])
def create_opt_dir(term, block):
    opt_dir = OptDir()
    return opt_dir


@rule(
    "service",
    "has",
    "opt-dir",
    description="""
Add docker compose options to the service that contain the volume mappings for the
opt dirs""",
)
def service_has_opt_dir(service, opt_dir):
    service.docker_compose_configs.add(
        DockerComposeConfig(
            lambda x: props.get_docker_compose_config(opt_dir), is_dev=True
        )
    )


@extend(OptDir)
class ExtendOptDir:
    render = MemFun(props.render_opt_dir)
    service = P.parent(Service, "has", "opt-dir")


class StoreOptPaths:
    opt_paths = P.tree(
        "has", "opt-path", merge=lambda acc, x: [*acc, x], initial=list()
    )
