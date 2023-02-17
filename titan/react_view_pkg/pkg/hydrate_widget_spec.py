from moonleap import get_session
from moonleap.blocks.term import str_to_term
from titan.react_view_pkg.pkg.preprocess_dps import get_dps_name

from .create_resource import create_resource


def hydrate_widget_spec(widget_spec):
    widget_spec.pipelines = list()
    widget_spec.named_props = list()
    widget_spec.named_default_props = list()

    block = widget_spec.root.component.meta.block
    _create_pipelines(widget_spec, block)
    _get_props(widget_spec, block)


def _create_pipelines(widget_spec, block):
    if pipeline_datas := widget_spec.get_value("pipelines", default={}):
        for pipeline_name, pipeline_data in pipeline_datas.items():
            pipeline = _create_pipeline(block, pipeline_name, pipeline_data)
            widget_spec.pipelines.append(pipeline)


def _create_pipeline(block, pipeline_name, pipeline_data):
    from titan.api_pkg.pipeline.resources import Pipeline

    pipeline = Pipeline(name=pipeline_name)
    for term_str in pipeline_data:
        term = dps_str_to_term(term_str)
        pipeline.resources.append(create_resource(block, term))

    return pipeline


def _get_props(widget_spec, block):
    for prop_name, prop_term_str in widget_spec.get_value("props", default={}).items():
        if term := str_to_term(prop_term_str):
            widget_spec.named_props.append(create_resource(block, term))

    for dps_value in widget_spec.get_value("dps", default=[]):
        term = dps_str_to_term("props." + dps_value)
        widget_spec.named_default_props.append(create_resource(block, term))


def dps_str_to_term(dps_value):
    lut = get_session().settings["dps_term_str_by_ts_var"]
    term = str_to_term(dps_value)
    if not term:
        dps_name = get_dps_name(dps_value)
        term_str = lut.get(dps_name)
        if not term_str:
            raise Exception(f"Dps term not found for {dps_name}. Check settings.py")
        term = str_to_term(term_str)
    return term
