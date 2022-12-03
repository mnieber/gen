def component_get_pipeline_and_data_path(component, named_output=None, term=None):
    for pipeline in component.pipelines:
        data_path = pipeline.data_path(named_output, term)
        if data_path:
            return pipeline, data_path
    return None, None


def component_maybe_expression(component, named_item_or_item_list):
    pipeline, data_path = component.get_pipeline_and_data_path(named_item_or_item_list)
    if not pipeline:
        return "'Moonleap Todo'"

    pipeline_source = pipeline.source
    if pipeline_source.meta.term.tag in ("query", "mutation"):
        return pipeline_source.name
    elif pipeline_source.meta.term.tag in ("props",):
        named_item = pipeline.elements[0].obj
        return f"props.{named_item.typ.item_name}"
    elif pipeline_source.meta.term.tag in ("state~provider",):
        item_or_item_list = pipeline.elements[0].obj
        if item_or_item_list.meta.term.tag in ("item", "item-list"):
            return f"state.{item_or_item_list.typ.ts_var}"
    else:
        raise Exception(f"Unknown pipeline source: {pipeline_source}")
