from moonleap.render.template_renderer import render_templates
from titan.react_module_pkg.apimutation.props import render_mutation_endpoint
from titan.react_module_pkg.apiquery.props import render_query_endpoint
from titan.react_module_pkg.schema.props import render_schema


def render(self, write_file, render_template, output_path):
    for query in self.graphql_api.queries:
        render_query_endpoint(self, query, write_file, render_template)

    for mutation in self.graphql_api.mutations:
        render_mutation_endpoint(self, mutation, write_file, render_template)

    for item_type in self.graphql_api.item_types:
        render_schema(self, item_type, write_file, render_template)

    for template_dir, get_context, skip_render in self.template_dirs:
        if not skip_render or not skip_render(self):
            render_templates(template_dir, get_context=get_context)(
                self, write_file, render_template, output_path
            )
