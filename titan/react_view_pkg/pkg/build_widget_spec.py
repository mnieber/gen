from moonleap import is_private_key
from moonleap.utils.fp import aperture
from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.get_builders import get_builders
from titan.react_view_pkg.pkg.hydrate_widget_spec import hydrate_widget_spec
from titan.widgetspec.div import Div


def build_widget_spec(widget_spec) -> BuilderOutput:
    root_widget_spec = widget_spec

    # Create widget_spec.div
    widget_spec.div = Div(
        styles=widget_spec.styles,
        attrs=_to_div_attrs(widget_spec.get_value("set", default={})),
    )

    # If there are wrapper widget specs W1, ..., Wn, then the widget spec
    # we must build is W1, where W1 has W2 as a child, W2 has W3 as a child, etc,
    # and Wn has the widget spec as a child.

    # Clear wrapper widget-specs, so that we'll only use them once.
    wrapper_widget_specs = list(widget_spec.wrapper_widget_specs)
    widget_spec.wrapper_widget_specs = []

    if wrapper_widget_specs:
        root_widget_spec = wrapper_widget_specs[0]
        for parent, child in aperture(2, wrapper_widget_specs + [widget_spec]):
            parent.add_child_widget_spec(child)

    result = BuilderOutput()
    builders = get_builders(root_widget_spec)
    assert builders

    # We hydrate the widget spec (also using the data that has
    # been added to it in preprocessing_widget_spec).
    hydrate_widget_spec(root_widget_spec)

    # Finally, we build the widget spec using the builders.
    for builder in builders:
        try:
            builder.build()
        except Exception as e:
            print(f"\nError building {widget_spec}")
            raise e
        result.merge(builder.output)

    # Restore wrapper widget-specs
    widget_spec.wrapper_widget_specs = wrapper_widget_specs

    return result


def _get_values(spec):
    result = {}
    for key, value in spec.items():
        if is_private_key(key):
            clean_key = key.removeprefix("__").removesuffix("__")
            result[clean_key] = value

    return result


def _to_div_attrs(attrs):
    return [f"{key}={value}" for key, value in attrs.items()]
