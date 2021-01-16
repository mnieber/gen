import moonleap.resource.props as P
from leap_mn.service import Service
from moonleap import MemFun, extend, tags

from . import props
from .resources import OptDir, OptPath  # noqa


@tags(["opt-dir"])
def create_opt_dir(term, block):
    opt_dir = OptDir()
    return opt_dir


class StoreOptPaths:
    opt_paths = P.tree(
        "has", "opt-path", merge=lambda acc, x: [*acc, x], initial=list()
    )


@extend(OptDir)
class ExtendOptDir:
    render = MemFun(props.render_opt_dir)
    service = P.parent(Service, "has", "opt-dir")
