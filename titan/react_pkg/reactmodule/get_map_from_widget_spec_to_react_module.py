import ramda as R


def get_map_from_widget_spec_to_react_module(widget_reg, react_modules):
    for react_module in react_modules:
        for component in react_module.components:
            if component.widget_spec:
                component.widget_spec.module_name = react_module.name

    widget_specs = [x for x in widget_reg.widget_specs()]
    known = list(widget_specs)
    lut = {}

    changed = True
    while changed:
        changed = False
        for widget_spec in list(widget_specs):
            for child_widget_spec in widget_spec.child_widget_specs:
                if child_widget_spec not in known:
                    changed = True
                    known.append(child_widget_spec)
                    widget_specs.append(child_widget_spec)

            if widget_spec.module_name:
                changed = True
                widget_specs.remove(widget_spec)

                react_module = R.head(
                    [x for x in react_modules if x.name == widget_spec.module_name]
                )
                if not react_module:
                    raise Exception(
                        f"React module not found: {widget_spec.module_name}"
                    )

                if widget_spec.is_component_def:
                    lut[widget_spec.widget_type] = react_module

                for child_widget_spec in widget_spec.child_widget_specs:
                    if not child_widget_spec.module_name:
                        child_widget_spec.module_name = widget_spec.module_name

    if len([x for x in widget_specs if x.is_component_def]):
        raise Exception(f"Could not determine module for widgets: {widget_specs}")

    return lut
