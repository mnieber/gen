from moonleap import append_uniq
from moonleap.blocks.term import match_term_to_pattern, word_to_term
from moonleap.utils.__init__ import remove_trailing_tildes
from titan.react_view_pkg.widgetregistry import get_widget_reg


def widget_spec_handler_terms(widget_spec):
    return widget_spec.src_dict.setdefault("__handlers__", [])


def widget_spec_bvr_names(widget_spec):
    return widget_spec.src_dict.setdefault("__bvrs__", [])


def widget_spec_field_names(widget_spec):
    result = []
    fields = widget_spec.src_dict.setdefault("__fields__", {})
    for field_name, fields in fields.items():
        for field in fields:
            clean_field_name = remove_trailing_tildes(field_name)
            prefix = "" if clean_field_name == "." else clean_field_name + "."
            result.append(f"{prefix}{field}")
    return result


def widget_spec_component(widget_spec):
    if not widget_spec.is_component:
        return None

    for component in get_widget_reg().components:
        if widget_term := word_to_term(widget_spec.widget_name):
            if match_term_to_pattern(component.meta.term, widget_term):
                return component

    raise Exception(f"Cannot find component for {widget_spec.widget_name}")


def widget_spec_maybe_expression(widget_spec, named_item_or_item_list):
    pipeline, data_path = _get_pipeline(widget_spec, named_item_or_item_list)
    if not pipeline:
        return "'Moonleap Todo'"
    return pipeline.maybe_expression(named_item_or_item_list)


def widget_spec_get_data_path(widget_spec, obj):
    pipeline, data_path = _get_pipeline(widget_spec, obj)
    if not data_path:
        for named_res_set in (widget_spec.named_props, widget_spec.named_default_props):
            for named_prop in named_res_set:
                t = obj.meta.term
                if match_term_to_pattern(named_prop.meta.term, t):
                    return f"props.{named_prop.typ.ts_var}"
    return data_path


def _get_pipeline(widget_spec, obj):
    try:
        results = []
        for pipeline in widget_spec.pipelines:
            if data_path := pipeline.data_path(obj):
                results.append((pipeline, data_path))

        if len(results) > 1:
            raise Exception("More than one data path found for " + f"{obj}: {results}")
        return results[0] if results else (None, None)
    except Exception as e:
        print(f"\nIn widget_spec {widget_spec}")
        raise


def widget_spec_get_pipeline_by_name(widget_spec, name):
    for pipeline in widget_spec.pipelines:
        if pipeline.name == name:
            return pipeline
    return None


def widget_spec_queries(widget_spec):
    result = []

    for pipeline in widget_spec.pipelines:
        pipeline_source = pipeline.source
        if pipeline_source.meta.term.tag == "query":
            append_uniq(result, pipeline_source)

    return result


def widget_spec_mutations(widget_spec):
    result = []

    for pipeline in widget_spec.pipelines:
        pipeline_source = pipeline.source
        if pipeline_source.meta.term.tag == "mutation":
            append_uniq(result, pipeline_source)

    return result
