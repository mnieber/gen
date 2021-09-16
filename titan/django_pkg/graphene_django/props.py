import os
from pathlib import Path

from moonleap import upper0
from moonleap.render.template_renderer import render_templates
from moonleap.utils.case import lower0

from .props_datatype import SectionsDataType
from .props_endpoint import SectionsMutation, SectionsQuery


def render(self, write_file, render_template):
    api_module = self.service.django_app.api_module

    sections_query = SectionsQuery(self)
    for query in api_module.graphql_api.queries:
        template_path = Path(__file__).parent / "templates_query"
        render_templates(
            template_path,
            query=query,
            sections=sections_query,
        )(self, write_file, render_template)

    sections_mutation = SectionsMutation(self)
    for mutation in api_module.graphql_api.mutations:
        template_path = Path(__file__).parent / "templates_mutation"
        render_templates(
            template_path,
            mutation=mutation,
            sections=sections_mutation,
        )(self, write_file, render_template)

    sections_datatype = SectionsDataType(self)
    for datatype in api_module.graphql_api.types:
        template_path = Path(__file__).parent / "templates_types"
        render_templates(
            template_path,
            item_name=lower0(datatype),
            sections=sections_datatype,
        )(self, write_file, render_template)

    template_path = Path(__file__).parent / "templates"
    render_templates(template_path)(self, write_file, render_template)


def _query_py_classname(query):
    return upper0(query.name) + "Query"


def _mutation_py_classname(mutation):
    return upper0(mutation.name)


class Sections:
    def __init__(self, res):
        self.res = res
        self.graphql_api = res.service.django_app.api_module.graphql_api

    def query_imports(self):
        result = []
        for query in self.graphql_api.queries:
            classname = _query_py_classname(query)
            result.append(f"from .{classname.lower()} import {classname}")

        return os.linesep.join(result)

    def query_base_classes(self):
        return ", ".join(
            [_query_py_classname(query) for query in self.graphql_api.queries]
        )

    def mutation_imports(self):
        result = []
        for mutation in self.graphql_api.mutations:
            classname = _mutation_py_classname(mutation)
            result.append(f"from .{classname.lower()} import {classname}")

        return os.linesep.join(result)

    def mutation_fields(self):
        result = []
        for mutation in self.graphql_api.mutations:
            result.append(
                f"    {mutation.name} = {_mutation_py_classname(mutation)}.Field()"
            )

        return os.linesep.join(result)
