import moonleap.props as P
from moonleap import extend, rule, tags
from moonleap.memfun import MemFun

from . import props as props
from .resources import OutputPath


class StoreOutputPaths:
    output_paths = P.tree(
        "has", "output-path", merge=props.merge, initial=OutputPath("")
    )
    set_output_path = MemFun(lambda self, path: self.output_paths.add(OutputPath(path)))
