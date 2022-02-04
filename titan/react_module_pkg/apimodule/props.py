from pathlib import Path

from moonleap.render.template_renderer import render_templates
from titan.react_module_pkg.apimutation.props import render_mutation_endpoint
from titan.react_module_pkg.apiquery.props import render_query_endpoint
from titan.react_module_pkg.schema.props import render_schema

from .type_context import get_context


def render(self, write_file, render_template, output_path):
    for query in self.graphql_api.queries:
        render_query_endpoint(self, query, write_file, render_template)

    for mutation in self.graphql_api.mutations:
        render_mutation_endpoint(self, mutation, write_file, render_template)

    render_schema(self, self.graphql_api.item_types, write_file, render_template)

    for item_type in self.graphql_api.item_types:
        render_type(self, item_type, write_file, render_template)

    for template_dir, get_context, skip_render in self.template_dirs:
        if not skip_render or not skip_render(self):
            render_templates(template_dir, get_context=get_context)(
                self, write_file, render_template, output_path
            )


def render_type(api_module, item_type, write_file, render_template):
    template_path = Path(__file__).parent / "type_templates"
    render_templates(template_path, get_context=lambda x: get_context(x))(
        item_type,
        write_file,
        render_template,
        output_path=api_module.merged_output_path,
    )
