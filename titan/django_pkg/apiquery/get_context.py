import os

from moonleap.typespec.field_spec import input_is_used_for_output
from moonleap.utils.case import sn
from moonleap.utils.codeblock import CodeBlock
from titan.django_pkg.graphene_django.utils import get_django_model_imports


def _get_resolve_expression(query, field_spec):
    filter_args = ", ".join(
        f"{sn(field_spec.short_name)}={sn(field_spec.short_name)}"
        for field_spec in query.inputs_type_spec.field_specs
    )

    if field_spec.field_type == "relatedSet":
        return (
            f"{field_spec.field_type_attrs['target']}.objects.filter"
            + f"({filter_args})"
        )

    if field_spec.field_type == "fk":
        return (
            f"{field_spec.field_type_attrs['target']}.objects.filter"
            + f"({filter_args}).first()"
        )

    if field_spec.field_type == "json":
        return "{}"

    if field_spec.field_type == "int":
        return "0"

    raise Exception(f"Could not deduce return value for type {field_spec.field_type}")


def get_context(query, api_module):
    _ = lambda: None
    _.query = query
    _.django_app = api_module.django_app
    _.inputs_type_spec = query.inputs_type_spec
    _.outputs_type_spec = query.outputs_type_spec
    _.input_field_specs = list(_.inputs_type_spec.field_specs)
    _.output_field_specs = list(_.outputs_type_spec.field_specs)

    class Sections:
        def query_imports(self):
            result = []
            type_specs = [_.outputs_type_spec]
            result.extend(get_django_model_imports(_.django_app, type_specs))

            return os.linesep.join(result)

        def declare_query_endpoints(self):
            root = CodeBlock(style="python", level=1)

            for output_field_spec in _.output_field_specs:
                endpoint_name = sn(output_field_spec.name)
                endpoint_args = ", ".join(
                    f"{sn(input_field_spec.short_name)}={input_field_spec.graphene_input_type}"
                    for input_field_spec in _.input_field_specs
                    if input_is_used_for_output(input_field_spec, output_field_spec)
                )

                root.abc(
                    f"{endpoint_name} = "
                    + f"{output_field_spec.graphene_output_type(endpoint_args)}"
                )

            return root.result

        def query_resolve_functions(self):
            indent = " " * 4
            result = []
            field_names = list([sn(x.short_name) for x in _.input_field_specs])

            for output_field_spec in _.output_field_specs:
                endpoint_name = sn(output_field_spec.name)
                resolve_function_args = ", ".join(["info"] + field_names)
                result.append(
                    f"{indent}def resolve_{endpoint_name}"
                    + f"(self, {resolve_function_args}):"
                )
                resolve_expression = _get_resolve_expression(query, output_field_spec)
                result.append(f"{indent}    return {resolve_expression}")

            return os.linesep.join(result)

    return dict(sections=Sections(), _=_)
