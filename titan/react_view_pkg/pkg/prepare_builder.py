def prepare_builder(builder):
    from titan.react_view_pkg.pkg.get_builder import get_builder

    builder.prepare()
    if builder.widget_spec.widget_base_type == "Children":
        builder.output.has_children = True

    if not builder.parent_builder or not builder.widget_spec.is_component_def:
        for child_widget_spec in builder.widget_spec.child_widget_specs:
            child_builder = get_builder(child_widget_spec, parent_builder=builder)
            prepare_builder(child_builder)
            builder.output.add(child_builder.output)
