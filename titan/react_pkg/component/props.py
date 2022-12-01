import os

from moonleap import create_forward, get_session, load_yaml
from moonleap.builder.add_meta_data_to_blocks import add_meta_data_to_blocks
from moonleap.parser.block_collector import create_block
from moonleap.verbs import connects, has

_pipelines = None


def get_pipelines():
    global _pipelines
    if _pipelines is None:
        spec_dir = get_session().spec_dir
        fn = os.path.join(spec_dir, "pipelines.yaml")
        _pipelines = load_yaml(fn) if os.path.exists(fn) else {}
    return _pipelines


def load_pipelines(component):
    pipelines = get_pipelines()
    forwards = []
    for component_term, component_data in pipelines.get("components", {}).items():
        _check_name(component_term)
        if component_term == component.meta.term.as_normalized_str:
            # Create a special block inside the component block for the pipelines.
            block = _create_pipelines_block(component)

            for pipeline_term_str, pipeline_data in component_data.get(
                "pipelines", {}
            ).items():
                # Create forwards to construct the pipeline.
                forwards.append(
                    create_forward(component, has, pipeline_term_str, block=block)
                )
                for term in pipeline_data:
                    forwards.append(
                        create_forward(pipeline_term_str, connects, term, block=block)
                    )
    return forwards


def component_get_pipeline_and_expr(component, named_output=None, term=None):
    for pipeline in component.pipelines:
        result_expr = pipeline.result_expression(named_output, term)
        if result_expr:
            return pipeline, result_expr
    return None, None


def component_maybe_expression(component, named_item_or_item_list):
    pipeline, expr = component.get_pipeline_and_expr(named_item_or_item_list)
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


def _check_name(name):
    if "_" in name or name != name.lower():
        raise Exception(f"Name should be in kebab-case: {name}")


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
