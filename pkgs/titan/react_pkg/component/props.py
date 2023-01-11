from moonleap import append_uniq
from moonleap.blocks.term import match_term_to_pattern


def component_get_data_path(component, obj):
    pipeline, data_path = _get_component_pipeline(component, obj)
    if not data_path:
        for named_res_set in (component.named_props, component.named_default_props):
            for named_prop in named_res_set:
                t = obj.meta.term
                if match_term_to_pattern(named_prop.meta.term, t):
                    return f"props.{named_prop.typ.ts_var}"
    return data_path


def _get_component_pipeline(component, obj):
    try:
        return get_pipeline_and_data_path(component.pipelines, obj)
    except Exception as e:
        print(f"\nIn component {component}")
        raise


def get_pipeline_and_data_path(pipelines, obj):
    results = []
    for pipeline in pipelines:
        if data_path := pipeline.data_path(obj):
            results.append((pipeline, data_path))

    if len(results) > 1:
        raise Exception("More than one data path found for " + f"{obj}: {results}")
    return results[0] if results else (None, None)


def component_maybe_expression(component, named_item_or_item_list):
    pipeline, data_path = _get_component_pipeline(component, named_item_or_item_list)
    if not pipeline:
        return "'Moonleap Todo'"
    return pipeline.maybe_expression(named_item_or_item_list)


def component_queries(component):
    result = []

    for pipeline in component.pipelines:
        pipeline_source = pipeline.source
        if pipeline_source.meta.term.tag == "query":
            append_uniq(result, pipeline_source)

    return result


def component_mutations(component):
    result = []

    for pipeline in component.pipelines:
        pipeline_source = pipeline.source
        if pipeline_source.meta.term.tag == "mutation":
            append_uniq(result, pipeline_source)

    return result
