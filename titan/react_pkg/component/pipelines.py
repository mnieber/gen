from moonleap import create_forward
from moonleap.blocks.parser.utils.get_meta import get_meta
from moonleap.blocks.verbs import connects, has, has_default_prop, has_prop
from moonleap.resources.named_resource import named
from titan.api_pkg.pipeline.resources import Pipeline


def get_pipeline_forwards(component):
    widget_spec = component.widget_spec
    forwards = []
    if not widget_spec:
        return forwards

    def _get_pipeline():
        pipeline = named(Pipeline)()
        pipeline.meta = get_meta("+:pipeline")
        pipeline.typ = Pipeline()
        return pipeline

    if pipeline_datas := widget_spec.src_dict.get("__pipelines__", {}):
        for pipeline_data in pipeline_datas:
            pipeline = _get_pipeline()
            forwards += [create_forward(component, has, pipeline)]
            for term_str in pipeline_data:
                forwards += [create_forward(pipeline, connects, term_str)]

    return forwards


def get_props_forwards(component):
    widget_spec = component.widget_spec
    forwards = []
    if not widget_spec:
        return forwards

    for prop_term_str in widget_spec.named_prop_terms:
        forwards += [create_forward(component, has_prop, prop_term_str)]

    for default_prop_term_str in widget_spec.named_default_prop_terms:
        forwards += [create_forward(component, has_default_prop, default_prop_term_str)]

    return forwards
