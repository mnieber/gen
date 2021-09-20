import os

from titan.django_pkg.graphene_django.utils import endpoint_imports


def _field_arg_type(field_spec, args):
    if field_spec.field_type == "related_set":
        return f"graphene.List({field_spec.fk_type_spec.tn_graphene}{args})"

    if field_spec.field_type == "fk":
        return f"graphene.Field({field_spec.fk_type_spec.tn_graphene}{args})"

    if field_spec.field_type == "boolean":
        return f"graphene.Boolean()"

    if field_spec.field_type == "string":
        return f"graphene.String()"

    if field_spec.field_type == "uuid":
        return f"graphene.ID()"

    if field_spec.field_type == "any":
        return f"GenericScalar"

    raise Exception(f"Cannot deduce arg type for {field_spec.field_type}")


def _endpoint_args(field_specs):
    result = {}
    for field_spec in field_specs:
        result[field_spec.name] = _field_arg_type(field_spec, "")
    return result


def _filter_args(query):
    return ", ".join(
        f"{field_name}={field_name}"
        for field_name in _endpoint_args(query.inputs_type_spec.field_specs).keys()
    )


def _return_value_for_field_spec(query, field_spec):
    if field_spec.field_type == "related_set":
        return (
            f"{field_spec.fk_type_spec.tn_django_model}.objects.filter"
            + f"({_filter_args(query)})"
        )

    if field_spec.field_type == "fk":
        return (
            f"{field_spec.fk_type_spec.tn_django_model}.objects.filter"
            + f"({_filter_args(query)}).first()"
        )

    raise Exception(f"Could not deduce return value for type {field_spec.field_type}")


class SectionsQuery:
    def __init__(self, res):
        self.res = res

    def query_imports(self, query):
        result = []
        item_names = set()
        for field_spec in list(query.inputs_type_spec.field_specs) + list(
            query.outputs_type_spec.field_specs
        ):
            result.extend(
                endpoint_imports(self.res.service.django_app, item_names, field_spec)
            )

        return os.linesep.join(result)

    def query_outputs(self, query):
        indent = " " * 4
        result = []

        for field_spec in query.outputs_type_spec.field_specs:
            args = ", ".join(
                f"{field_name}={arg}"
                for field_name, arg in _endpoint_args(
                    query.inputs_type_spec.field_specs
                ).items()
            )
            if args:
                args = ", " + args
            result.append(
                f"{indent}{field_spec.name_snake} = {_field_arg_type(field_spec, args)}"
            )

        return os.linesep.join(result)

    def query_resolve_functions(self, query):
        indent = " " * 4
        result = []
        field_names = list([x.name for x in query.inputs_type_spec.field_specs])

        for field_spec in query.outputs_type_spec.field_specs:
            result.append(
                f"{indent}def resolve_{field_spec.name_snake}(self, {', '.join(['info'] + field_names)}):"
            )
            result.append(
                f"{indent}  return {_return_value_for_field_spec(query, field_spec)}"
            )

        return os.linesep.join(result)
