from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.get_builders import get_builders
from titan.react_view_pkg.pkg.hydrate_widget_spec import hydrate_widget_spec


def build_widget_spec(widget_spec) -> BuilderOutput:
    result = BuilderOutput()
    builders = get_builders(widget_spec)
    assert builders

    # We hydrate the widget spec (also using the data that has
    # been added to it in preprocessing_widget_spec).
    hydrate_widget_spec(widget_spec)

    # Finally, we build the widget spec using the builders.
    for builder in builders:
        try:
            builder.build()
        except Exception as e:
            print(f"\nError building {widget_spec}")
            raise e
        result.merge(builder.output)
    return result
