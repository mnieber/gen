import moonleap.resource.props as P
from moonleap.verbs import has

from . import props as props


class StoreOutputPaths:
    output_paths = P.tree(has, "output-path")
    output_path = props.output_path(has, "output-path")
    merged_output_path = props.merged_output_path()
