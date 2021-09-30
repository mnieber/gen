from moonleap.render.template_renderer import render_templates
from titan.api_pkg.typeregistry import TypeRegistry
from titan.django_pkg.apimutation.props import render_mutation_endpoint
from titan.django_pkg.apiquery.props import render_query_endpoint
from titan.django_pkg.schema.props import render_schema


def render(self, write_file, render_template, output_path):
    # TODO: use query.add_template_dir
    for query in self.graphql_api.queries:
        render_query_endpoint(self, query, write_file, render_template)

    for mutation in self.graphql_api.mutations:
        render_mutation_endpoint(self, mutation, write_file, render_template)

    for item_type in TypeRegistry(self.graphql_api).get_item_types():
        render_schema(self, item_type, write_file, render_template)

    for template_dir, get_context, skip_render in self.template_dirs:
        if not skip_render or not skip_render(self):
            render_templates(template_dir, get_context=get_context)(
                self, write_file, render_template, output_path
            )
