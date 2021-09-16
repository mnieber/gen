import os

from titan.django_pkg.graphene_django.utils import (
    endpoint_args,
    endpoint_imports,
    field_arg_type,
)


def _filter_args(query):
    return ", ".join(
        f"{field_name}={field_name}"
        for field_name in endpoint_args(
            query.inputs_type_spec.field_spec_by_name
        ).keys()
    )


def _return_value_for_field_spec(query, field_spec):
    if field_spec.field_type == "list":
        return (
            f"{field_spec.fk_type_spec.tn_django_model}.objects.filter"
            + f"({_filter_args(query)})"
        )

    if field_spec.field_type == "fk":
        return (
            f"{field_spec.fk_type_spec.tn_django_model}.objects.filter"
            + f"({_filter_args(query)}).first()"
        )

    return "'hello'"


class SectionsQuery:
    def __init__(self, res):
        self.res = res

    def query_imports(self, query):
        result = []
        item_names = set()
        for (field_name, field_spec) in list(
            query.inputs_type_spec.field_spec_by_name.items()
        ) + list(query.outputs_type_spec.field_spec_by_name.items()):
            result.extend(
                endpoint_imports(self.res.service.django_app, item_names, field_spec)
            )

        return os.linesep.join(result)

    def query_outputs(self, query):
        indent = " " * 4
        result = []

        for (
            field_name,
            field_spec,
        ) in query.outputs_type_spec.field_spec_by_name.items():
            args = ", ".join(
                f"{field_name}={arg}"
                for field_name, arg in endpoint_args(
                    query.inputs_type_spec.field_spec_by_name
                ).items()
            )
            if args:
                args = ", " + args
            result.append(
                f"{indent}{field_spec.name_snake} = {field_arg_type(field_spec, args)}"
            )

        return os.linesep.join(result)

    def query_resolve_functions(self, query):
        indent = " " * 4
        result = []
        field_names = list(query.inputs_type_spec.field_spec_by_name.keys())

        for (
            field_name,
            field_spec,
        ) in query.outputs_type_spec.field_spec_by_name.items():
            result.append(
                f"{indent}def resolve_{field_spec.name_snake}(self, {', '.join(['info'] + field_names)}):"
            )
            result.append(
                f"{indent}  return {_return_value_for_field_spec(query, field_spec)}"
            )

        return os.linesep.join(result)
