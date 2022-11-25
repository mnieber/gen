from titan.react_view_pkg.pkg.get_margins import get_margins


def add_child_widgets(builder, child_widget_specs):
    for child_widget_spec in child_widget_specs:
        if child_widget_spec.widget_base_type == "Children":
            builder.output.has_children = True

    prev_widget_spec = None
    for child_widget_spec in child_widget_specs:
        child_builder = get_child_widget_builder(
            builder, child_widget_spec, builder.level + 1
        )
        margins = get_margins(prev_widget_spec, child_widget_spec)
        child_builder.build(margins)
        builder.output.add(child_builder.output)
        prev_widget_spec = child_widget_spec


def get_child_widget_builder(builder, child_widget_spec, level):
    from titan.react_view_pkg.pkg.get_builder import get_builder

    # Look up builder_type in luts
    b = builder
    while b:
        builder_type = b.builder_type_lut.get(child_widget_spec.widget_base_type, None)
        if builder_type:
            return builder_type(child_widget_spec, builder, level)
        b = b.parent_builder

    return get_builder(child_widget_spec, builder, level)
