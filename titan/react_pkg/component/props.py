from moonleap.parser.term import match_term_to_pattern


def component_get_data_path(component, obj=None, term=None):
    pipeline, data_path = _get_component_pipeline(component, obj, term)
    if not data_path:
        for named_res_set in (component.named_props, component.named_default_props):
            for named_prop in named_res_set:
                t = obj.meta.term if obj else term
                if match_term_to_pattern(named_prop.meta.term, t):
                    return f"props.{named_prop.typ.ts_var}"
    return data_path


def _get_component_pipeline(component, obj=None, term=None):
    try:
        return get_pipeline_and_data_path(component.pipelines, obj, term)
    except Exception as e:
        print(f"\nIn component {component}")
        raise


def get_pipeline_and_data_path(pipelines, obj=None, term=None):
    results = []
    for pipeline in pipelines:
        if data_path := pipeline.data_path(obj, term):
            results.append((pipeline, data_path))

    if len(results) > 1:
        raise Exception("More than one data path found for " + f"{obj}: {results}")
    return results[0] if results else (None, None)


def component_maybe_expression(component, named_item_or_item_list):
    pipeline, data_path = _get_component_pipeline(component, named_item_or_item_list)
    if not pipeline:
        return "'Moonleap Todo'"
    return pipeline.maybe_expression(named_item_or_item_list)


def load_component(component):
    from titan.react_pkg.packages.use_react_packages import use_react_packages
    from titan.react_view_pkg.pkg.build import build

    if widget_spec := component.widget_spec:
        react_app = component.module.react_app
        component.build_output = build(widget_spec)

        for (
            module_name,
            packages,
        ) in component.build_output.react_packages_by_module_name.items():
            use_react_packages(react_app.get_module(module_name), packages)
