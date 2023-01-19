from moonleap.blocks.term import word_to_term

from .create_resource import create_resource


def hydrate_widget_spec(widget_spec):
    widget_spec.pipelines = list()
    widget_spec.named_props = list()
    widget_spec.named_default_props = list()

    block = widget_spec.root.component.meta.block
    _create_pipelines(widget_spec, block)
    _get_props(widget_spec, block)


def _create_pipelines(widget_spec, block):
    if pipeline_datas := widget_spec.src_dict.get("__pipelines__", {}):
        for pipeline_name, pipeline_data in pipeline_datas.items():
            pipeline = _create_pipeline(block, pipeline_name, pipeline_data)
            widget_spec.pipelines.append(pipeline)


def _create_pipeline(block, pipeline_name, pipeline_data):
    from titan.api_pkg.pipeline.resources import Pipeline

    pipeline = Pipeline(name=pipeline_name)
    for term_str in pipeline_data:
        pipeline.resources.append(create_resource(block, word_to_term(term_str)))

    return pipeline


def _get_props(widget_spec, block):
    for prop_term_str in widget_spec.src_dict.get("__props__", []):
        widget_spec.named_props.append(
            create_resource(block, word_to_term(prop_term_str))
        )

    for default_prop_term_str in widget_spec.src_dict.get("__default_props__", []):
        widget_spec.named_default_props.append(
            create_resource(block, word_to_term(default_prop_term_str))
        )
