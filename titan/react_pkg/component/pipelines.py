import ramda as R

from moonleap import create_forward
from moonleap.builder.add_meta_data_to_blocks import add_meta_data_to_blocks
from moonleap.parser.block_collector import create_block
from moonleap.verbs import connects, has, has_default_prop, has_prop


def get_pipeline_forwards(component):
    widget_spec = component.widget_spec
    forwards = []
    if not widget_spec:
        return forwards

    # Create a special block inside the component block for the pipelines.
    _block = None
    _pipeline_terms = []

    def get_block():
        nonlocal _block
        if _block is None:
            _block = _create_pipelines_block(component)
        return _block

    def _connect(pipeline_term_str, elm_term_str):
        return create_forward(
            pipeline_term_str, connects, elm_term_str, block=get_block()
        )

    def _add_pipeline(pipeline_term_str):
        nonlocal _pipeline_terms
        if pipeline_term_str in _pipeline_terms:
            raise Exception(f"Duplicate pipeline term: {pipeline_term_str}")

        _pipeline_terms.append(pipeline_term_str)
        return create_forward(component, has, pipeline_term_str, block=get_block())

    if pipeline_datas := widget_spec.src_dict.get("__pipelines__", {}):
        for pipeline_data in pipeline_datas:
            pipeline_term_str = _get_pipeline_term_str(pipeline_data[-1])
            forwards += [_add_pipeline(pipeline_term_str)]
            for term_str in pipeline_data:
                forwards += [_connect(pipeline_term_str, term_str)]

    return forwards


def _get_pipeline_term_str(data_name):
    name = data_name.replace("+", "-").replace(":", "-").replace("~", "-")
    return f"{name}+:pipeline"


def _create_pipelines_block(component):
    parent_block = component.meta.block
    block = create_block(
        f"{component.id}_pipelines",
        parent_block.level + 1,
        parent_block,
        [],
    )
    add_meta_data_to_blocks([block])
    return block


def get_props_forwards(component):
    widget_spec = component.widget_spec
    forwards = []
    if not widget_spec:
        return forwards

    for prop_term_str in widget_spec.named_props:
        forwards += [create_forward(component, has_prop, prop_term_str)]

    for default_prop_term_str in widget_spec.named_default_props:
        forwards += [create_forward(component, has_default_prop, default_prop_term_str)]

    return forwards
