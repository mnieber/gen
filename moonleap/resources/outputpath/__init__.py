import moonleap.resource.props as P

from . import props as props
from .resources import OutputPath  # noqa


class StoreOutputPaths:
    output_paths = P.tree("has", "output-path")
    output_path = props.output_path("has", "output-path")
