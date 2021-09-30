import os
from pathlib import Path

from moonleap import render_templates, u0
from titan.django_pkg.graphene_django.utils import (
    endpoint_imports_api,
    endpoint_imports_models,
)
from titan.react_module_pkg.apiquery.graphql_args import graphql_args


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
            f"{u0(field_spec.field_type_attrs['target'])}.objects.filter"
            + f"({_filter_args(query)})"
        )

    if field_spec.field_type == "fk":
        return (
            f"{u0(field_spec.field_type_attrs['target'])}.objects.filter"
            + f"({_filter_args(query)}).first()"
        )

    raise Exception(f"Could not deduce return value for type {field_spec.field_type}")


def get_context(query, api_module):
    _ = lambda: None
    _.django_app = api_module.django_app
    _.inputs_type_spec = query.inputs_type_spec
    _.outputs_type_spec = query.outputs_type_spec
    _.input_field_specs = list(_.inputs_type_spec.field_specs)
    _.output_field_specs = list(_.outputs_type_spec.field_specs)

    class Sections:
        def query_imports(self):
            result = []
            type_specs = [_.inputs_type_spec, _.outputs_type_spec]
            result.extend(endpoint_imports_api(type_specs))
            result.extend(endpoint_imports_models(_.django_app, type_specs))

            return os.linesep.join(result)

        def query_outputs(self):
            indent = " " * 4
            result = []

            for field_spec in _.output_field_specs:
                args = ", ".join(
                    f"{field_name}={arg}"
                    for field_name, arg in _endpoint_args(_.input_field_specs).items()
                )
                if args:
                    args = ", " + args
                result.append(
                    f"{indent}{field_spec.name_snake} = {_field_arg_type(field_spec, args)}"
                )

            return os.linesep.join(result)

        def query_resolve_functions(self):
            indent = " " * 4
            result = []
            field_names = list([x.name for x in _.input_field_specs])

            for field_spec in _.output_field_specs:
                result.append(
                    f"{indent}def resolve_{field_spec.name_snake}(self, {', '.join(['info'] + field_names)}):"
                )
                result.append(
                    f"{indent}    return {_return_value_for_field_spec(query, field_spec)}"
                )

            return os.linesep.join(result)

        def create_query_args(self):
            inputs = list(f"{x.name_snake}" for x in _.input_field_specs)
            outputs = list(f"{x.name_snake}_outputs=None" for x in _.output_field_specs)
            return ", ".join(inputs + outputs)

        def graphql_args(self, before):
            return graphql_args(_.input_field_specs, before, base_indent=6)

    return dict(sections=Sections(), _=_)


def render_query_endpoint(api_module, query, write_file, render_template):
    template_path = Path(__file__).parent / "templates"
    render_templates(template_path, get_context=lambda x: get_context(x, api_module))(
        query, write_file, render_template, output_path=api_module.merged_output_path
    )
