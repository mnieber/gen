from titan.react_view_pkg.pkg.get_margins import get_margins


def add_child_widgets(builder, child_widget_specs):
    from titan.react_view_pkg.pkg.get_builder import get_builder

    prev_widget_spec = None
    for child_widget_spec in child_widget_specs:
        child_builder = get_builder(child_widget_spec, parent_builder=builder)
        margins = get_margins(prev_widget_spec, child_widget_spec)
        child_builder.prepare()
        child_builder.build(margins)
        builder.output.add(child_builder.output)
        prev_widget_spec = child_widget_spec
