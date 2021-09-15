import os
from pathlib import Path

from moonleap import upper0
from moonleap.render.template_renderer import render_templates
from moonleap.utils.case import lower0
from titan.django_pkg.graphene_django.props_datatype import SectionsDataType
from titan.django_pkg.graphene_django.props_endpoint import SectionsEndpoint


def render(self, write_file, render_template):
    api_module = self.service.django_app.api_module
    sections = SectionsEndpoint(self)

    for query in api_module.graphql_api.queries:
        template_path = Path(__file__).parent / "templates_query"
        render_templates(template_path, query=query, sections=sections)(
            self, write_file, render_template
        )

    for mutation in api_module.graphql_api.mutations:
        template_path = Path(__file__).parent / "templates_mutation"
        render_templates(template_path, mutation=mutation, sections=sections)(
            self, write_file, render_template
        )

    for datatype in api_module.graphql_api.types:
        template_path = Path(__file__).parent / "templates_types"
        render_templates(
            template_path, item_name=lower0(datatype), sections=SectionsDataType(self)
        )(self, write_file, render_template)

    template_path = Path(__file__).parent / "templates"
    render_templates(template_path)(self, write_file, render_template)


def has_graphql_mutations(module):
    return bool(module.forms or module.items_received)


def has_graphql_queries(module):
    return bool(module.item_lists_provided)


class Sections:
    def __init__(self, res):
        self.res = res

    def query_imports(self):
        result = []
        graphql_api = self.res.service.django_app.api_module.graphql_api
        for query in graphql_api.queries:
            result.append(
                f"from .{query.name.lower()}query import {upper0(query.name)}Query"
            )

        return os.linesep.join(result)

    def query_base_classes(self):
        result = []
        graphql_api = self.res.service.django_app.api_module.graphql_api
        for query in graphql_api.queries:
            result.append(f"{upper0(query.name)}Query")

        return ", ".join(result)

    def mutation_imports(self):
        result = []
        graphql_api = self.res.service.django_app.api_module.graphql_api
        for mutation in graphql_api.mutations:
            result.append(
                f"from .{mutation.name.lower()} import {upper0(mutation.name)}"
            )

        return os.linesep.join(result)

    def mutation_fields(self):
        result = []
        graphql_api = self.res.service.django_app.api_module.graphql_api
        for mutation in graphql_api.mutations:
            result.append(f"    {mutation.name} = {upper0(mutation.name)}.Field()")

        return os.linesep.join(result)
