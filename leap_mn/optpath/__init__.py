import moonleap.props as P
from moonleap import Prop, extend
from moonleap.memfun import MemFun

from . import props
from .resources import OptPath


class StoreOptPaths:
    select_all_opt_paths = MemFun(props.select_all_opt_paths)
    opt_paths = P.children("has", "opt-path")
    opt_path_sources = P.children("has", "opt-path-source")
