from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.get_builders import get_builders


def build(widget_spec) -> BuilderOutput:
    result = BuilderOutput()
    builders = get_builders(widget_spec)
    assert builders
    for builder in builders:
        builder.build()
        result.add(builder.output)
    return result
