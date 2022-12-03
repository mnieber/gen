import os

import ramda as R

from moonleap import create_forward, get_session, load_yaml
from moonleap.builder.add_meta_data_to_blocks import add_meta_data_to_blocks
from moonleap.parser.block_collector import create_block
from moonleap.parser.term import match_term_to_pattern, word_to_term
from moonleap.verbs import connects, has, has_default_prop, has_prop

_pipelines = None


def get_pipelines():
    global _pipelines
    if _pipelines is None:
        spec_dir = get_session().spec_dir
        fn = os.path.join(spec_dir, "pipelines.yaml")
        _pipelines = load_yaml(fn) if os.path.exists(fn) else {}
    return _pipelines


def component_load_pipelines(component):
    pipelines = get_pipelines()
    pipeline_terms = []
    forwards = []

    for component_term_str, component_data in pipelines.get("components", {}).items():
        _check_name(component_term_str)
        component_term = word_to_term(component_term_str)
        if match_term_to_pattern(component.meta.term, component_term):
            # Create a special block inside the component block for the pipelines.
            block = _create_pipelines_block(component)

            def _connect(pipeline_term_str, elm_term_str):
                return create_forward(
                    pipeline_term_str, connects, elm_term_str, block=block
                )

            def _add_pipeline(pipeline_term_str):
                if pipeline_term_str in pipeline_terms:
                    raise Exception(f"Duplicate pipeline term: {pipeline_term_str}")
                pipeline_terms.append(pipeline_term_str)
                return create_forward(component, has, pipeline_term_str, block=block)

            for pipeline_data in component_data.get("pipelines", []):
                pipeline_term_str = _get_pipeline_term_str(pipeline_data[-1])
                forwards += [_add_pipeline(pipeline_term_str)]

                # Maybe insert a "props" pipeline source
                head_term = word_to_term(R.head(pipeline_data))
                if head_term and head_term.tag in ("item", "item~list"):
                    forwards += [_connect(pipeline_term_str, ":props")]

                # Add terms to the pipeline
                for term_str in pipeline_data:
                    forwards += [_connect(pipeline_term_str, term_str)]

            for propsKey, verb in (
                ("props", has_prop),
                ("defaultProps", has_default_prop),
            ):
                for prop_term_str in component_data.get(propsKey, []):
                    # Add prop to the component
                    forwards += [
                        create_forward(component_term_str, verb, prop_term_str)
                    ]

                    # Also add a pipeline that produces the prop value
                    pipeline_term_str = _get_pipeline_term_str(prop_term_str)
                    forwards += [_add_pipeline(pipeline_term_str)]
                    forwards += [
                        _connect(pipeline_term_str, ":props"),
                        _connect(pipeline_term_str, prop_term_str),
                    ]

    return forwards


def _get_pipeline_term_str(data_name):
    name = data_name.replace("+", "-").replace(":", "-").replace("~", "-")
    return f"{name}+:pipeline"


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
