import os

from moonleap import upper0


def _query_py_classname(query):
    return upper0(query.name) + "Query"


def _mutation_py_classname(mutation):
    return upper0(mutation.name)


class Sections:
    def __init__(self, res):
        self.res = res
        self.graphql_api = res.service.django_app.api_module.graphql_api
        self.modules = [
            module
            for module in res.service.django_app.modules
            if module.has_graphql_schema
        ]

    def query_imports(self):
        result = []
        for query in self.graphql_api.queries:
            classname = _query_py_classname(query)
            result.append(f"from .{classname.lower()} import {classname}")

        for module in self.modules:
            if module.has_graphql_schema:
                result.append(f"import {module.name}.schema")

        return os.linesep.join(result)

    def query_base_classes(self):
        return ", ".join(
            [f"{module.name}.schema.Query" for module in self.modules]
            + [_query_py_classname(query) for query in self.graphql_api.queries]
            + ["graphene.ObjectType"]
        )

    def mutation_base_classes(self):
        if not self.modules:
            return ""
        return (
            ", ".join([f"{module.name}.schema.Mutation" for module in self.modules])
            + ", "
        )

    def mutation_imports(self):
        result = []
        for mutation in self.graphql_api.mutations:
            classname = _mutation_py_classname(mutation)
            result.append(f"from .{classname.lower()} import {classname}")

        for module in self.modules:
            if module.has_graphql_schema:
                result.append(f"import {module.name}.schema")

        return os.linesep.join(result)

    def mutation_fields(self):
        result = []
        for mutation in self.graphql_api.mutations:
            result.append(
                f"    {mutation.name} = {_mutation_py_classname(mutation)}.Field()"
            )

        return os.linesep.join(result)


def get_context(self):
    return dict(sections=Sections(self))
