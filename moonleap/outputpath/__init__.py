import moonleap.resource.props as P

from . import props as props


class StoreOutputPaths:
    output_paths = P.tree("p-has", "output-path")
    output_path = props.output_path("p-has", "output-path")
    merged_output_path = props.merged_output_path()
