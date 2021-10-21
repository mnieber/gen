import moonleap.resource.props as P
from moonleap.resource.memfield import MemField

from . import props as props


class StoreOutputPaths:
    output_paths = P.tree("output_paths")
    output_path = props.output_path()
    merged_output_path = props.merged_output_path()
