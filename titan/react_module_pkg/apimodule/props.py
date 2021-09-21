import os
from pathlib import Path

from moonleap.render.template_renderer import render_templates
from moonleap.utils.case import lower0

from .endpoint import get_endpoint_mutation_text, get_endpoint_query_text
from .sections_datatype import SectionsDataType
from .sections_mutation import SectionsMutation
from .sections_query import SectionsQuery


def render(self, write_file, render_template):
    sections_datatype = SectionsDataType(self)

    sections_query = SectionsQuery(self)
    for query in self.graphql_api.queries:
        template_path = Path(__file__).parent / "templates_query"
        render_templates(
            template_path,
            query=query,
            outputs_item_name=lower0(query.outputs_type_spec.type_name),
            sections=sections_query,
            sections_datatype=sections_datatype,
        )(self, write_file, render_template)

    sections_mutation = SectionsMutation(self)
    for mutation in self.graphql_api.mutations:
        template_path = Path(__file__).parent / "templates_mutation"
        render_templates(
            template_path,
            mutation=mutation,
            outputs_item_name=lower0(mutation.outputs_type_spec.type_name),  # HACK
            sections=sections_mutation,
            sections_datatype=sections_datatype,
        )(self, write_file, render_template)

    for type_spec in self.graphql_api.data_type_specs:
        template_path = Path(__file__).parent / "templates_schemas"
        render_templates(
            template_path,
            item_name=lower0(type_spec.type_name),  # HACK
            sections=sections_datatype,
        )(self, write_file, render_template)

    template_path = Path(__file__).parent / "templates"
    render_templates(template_path)(self, write_file, render_template)


class Sections:
    def __init__(self, res):
        self.res = res
        self.graphql_api = res.graphql_api

    def queries(self):
        result = []

        for query in self.graphql_api.queries:
            text = get_endpoint_query_text(query)
            result.append(text)

        return os.linesep.join(result)

    def mutations(self):
        result = []

        for mutation in self.graphql_api.mutations:
            text = get_endpoint_mutation_text(mutation)
            result.append(text)

        return os.linesep.join(result)
