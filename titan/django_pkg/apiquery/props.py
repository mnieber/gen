from pathlib import Path

from moonleap import render_templates

from .get_context import get_context
from .get_context_test import get_context_test


def render_query_endpoint(api_module, query, write_file, render_template):
    render_templates(
        Path(__file__).parent / "templates",
        get_context=lambda x: get_context(x, api_module),
    )(query, write_file, render_template, output_path=api_module.merged_output_path)
    render_templates(
        Path(__file__).parent / "templates_test",
        get_context=lambda x: get_context_test(x, api_module),
    )(query, write_file, render_template, output_path=api_module.merged_output_path)
