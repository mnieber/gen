from titan.react_view_pkg.pkg.get_margins import get_margins


def add_child_widgets(builder, child_widget_specs):
    from titan.react_view_pkg.pkg.build import build

    prev_widget_spec = None
    for child_widget_spec in child_widget_specs:
        if child_widget_spec.place:
            continue
        margins = get_margins(prev_widget_spec, child_widget_spec)
        # TODO: use margins in child widget
        builder.output.add(build(child_widget_spec))
        prev_widget_spec = child_widget_spec
