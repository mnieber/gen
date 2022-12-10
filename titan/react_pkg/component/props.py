from moonleap.parser.term import match_term_to_pattern


def component_get_data_path(component, named_output=None, term=None):
    pipeline, data_path = _get_pipeline(component, named_output, term)
    if not data_path:
        for named_res_set in (component.named_props, component.named_default_props):
            for named_prop in named_res_set:
                t = named_output.meta.term if named_output else term
                if match_term_to_pattern(named_prop.meta.term, t):
                    return f"props.{named_prop.typ.ts_var}"
    return data_path


def _get_pipeline(component, named_output=None, term=None):
    results = []
    for pipeline in component.pipelines:
        if data_path := pipeline.data_path(named_output, term):
            results.append((pipeline, data_path))

    if len(results) > 1:
        raise Exception(
            f"More than one data path found for {named_output} in {component}: {results}"
        )
    return results[0] if results else (None, None)


def component_maybe_expression(component, named_item_or_item_list):
    pipeline, data_path = _get_pipeline(component, named_item_or_item_list)
    if not pipeline:
        return "'Moonleap Todo'"

    pipeline_source = pipeline.source
    if pipeline_source.meta.term.tag in ("query", "mutation"):
        return pipeline_source.name
    elif pipeline_source.meta.term.tag in ("props",):
        named_item = pipeline.elements[0].obj
        if (
            named_item.name == named_item_or_item_list.name
            and named_item.typ == named_item_or_item_list.typ
        ):
            return None
        return f"props.{named_item.typ.item_name}"
    elif pipeline_source.meta.term.tag in ("state~provider",):
        item_or_item_list = pipeline.elements[0].obj
        if item_or_item_list.meta.term.tag in ("item", "item-list"):
            return f"state.{item_or_item_list.typ.ts_var}"
    else:
        raise Exception(f"Unknown pipeline source: {pipeline_source}")


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
