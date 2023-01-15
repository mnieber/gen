from moonleap.utils.merge_into_config import merge_into_config
from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.get_builders import get_builders
from titan.react_view_pkg.pkg.hydrate_widget_spec import hydrate_widget_spec
from titan.react_view_pkg.widgetregistry import get_widget_reg
from titan.widgetspec.load_widget_specs.widget_spec_parser import WidgetSpecParser


def build_widget_spec(widget_spec) -> BuilderOutput:
    x = widget_spec.widget_name, widget_spec.is_component_def
    result = BuilderOutput()
    builders = get_builders(widget_spec)
    assert builders

    # First, we apply the widget spec extensions from all builders
    places = _get_places(widget_spec.src_dict)
    for builder in builders:
        if extension := builder.get_spec_extension(places):
            private_fields = {}
            for key, value in extension.items():
                if key.startswith("__"):
                    private_fields[key] = value
            merge_into_config(widget_spec.src_dict, private_fields)

            parser = WidgetSpecParser(widget_spec.module_name, get_widget_reg())
            parser.parse(extension, parent_widget_spec=widget_spec)

    # Then, we allow each builder to update the widget spec
    for builder in builders:
        builder.update_widget_spec()

    # Then, we hydrate the widget spec (also using the data that has
    # been added to it by the builders).
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


def _get_places(spec):
    places = []
    for key in spec.keys():
        parts = key.split(" with ")
        if len(parts) == 2 and key.startswith(parts[0] + " with "):
            places.append(parts[0])

    return places
