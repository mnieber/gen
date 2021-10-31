import os

from moonleap import u0
from moonleap.utils.join import join


def _query_py_classname(query):
    return u0(query.name) + "Query"


def _mutation_py_classname(mutation):
    return u0(mutation.name)


def get_context(graphene_django):
    _ = lambda: None
    _.django_app = graphene_django.service.django_app
    _.graphql_api = _.django_app.api_module.graphql_api
    _.modules = [module for module in _.django_app.modules if module.has_graphql_schema]

    class Sections:
        def graphene_query_imports(self):
            result = []
            for query in _.graphql_api.queries:
                classname = _query_py_classname(query)
                result.append(f"from .{classname.lower()} import {classname}")

            for module in _.modules:
                if module.has_graphql_schema:
                    result.append(f"import {module.name}.schema")

            return os.linesep.join(result)

        def query_base_classes(self):
            return ", ".join(
                [f"{module.name}.schema.Query" for module in _.modules]
                + [_query_py_classname(query) for query in _.graphql_api.queries]
                + ["graphene.ObjectType"]
            )

        def mutation_base_classes(self):
            return join(
                "",
                ", ".join([f"{module.name}.schema.Mutation" for module in _.modules]),
                ", ",
            )

        def mutation_imports(self):
            result = []
            for mutation in _.graphql_api.mutations:
                classname = _mutation_py_classname(mutation)
                result.append(f"from .{classname.lower()} import {classname}")

            for module in _.modules:
                if module.has_graphql_schema:
                    result.append(f"import {module.name}.schema")

            return os.linesep.join(result)

        def mutation_fields(self):
            result = []
            for mutation in _.graphql_api.mutations:
                result.append(
                    f"    {mutation.name} = {_mutation_py_classname(mutation)}.Field()"
                )

            return os.linesep.join(result)

    return dict(sections=Sections())
