import os
from pathlib import Path

from moonleap import render_templates, u0
from titan.django_pkg.graphene_django.utils import endpoint_imports


def graphene_type_from_field_spec(field_spec, args):
    if field_spec.field_type == "related_set":
        return f"graphene.List({field_spec.fk_type_spec.tn_graphene}{args})"

    if field_spec.field_type in ("form"):
        return f"{field_spec.fk_type_spec.tn_graphene}({args})"

    if field_spec.field_type == "boolean":
        return f"graphene.Boolean()"

    if field_spec.field_type in ("string", "slug"):
        return f"graphene.String()"

    if field_spec.field_type == "uuid":
        return f"graphene.ID()"

    if field_spec.field_type == "any":
        return f"GenericScalar"

    raise Exception(f"Cannot deduce arg type for {field_spec.field_type}")


def _mutation_arguments(field_specs):
    result = {}
    for field_spec in field_specs:
        result[field_spec.name_snake] = graphene_type_from_field_spec(
            field_spec, f"required={field_spec.required}"
        )
    return result


def get_context(mutation, api_module):
    _ = lambda: None
    _.django_app = api_module.django_app
    _.inputs_type_spec = mutation.inputs_type_spec
    _.outputs_type_spec = mutation.outputs_type_spec
    _.input_field_specs = list(_.inputs_type_spec.field_specs)
    _.output_field_specs = list(_.outputs_type_spec.field_specs)

    class Sections:
        def mutation_imports(self):
            result = []
            item_names = set()
            for field_spec in _.input_field_specs + _.output_field_specs:
                result.extend(endpoint_imports(_.django_app, item_names, field_spec))

            return os.linesep.join(result)

        def mutation_outputs(self):
            indent = " " * 4
            result = []

            for field_spec in _.output_field_specs:
                args = ""
                result.append(
                    f"{indent}{field_spec.name} = {graphene_type_from_field_spec(field_spec, args)}"
                )

            return os.linesep.join(result)

        def mutation_arguments(self):
            indent = " " * 8
            result = []

            args = _mutation_arguments(_.input_field_specs)
            for field_name, arg in args.items():
                result.append(f"{indent}{field_name} = {arg}")
            if not args:
                result.append(f"{indent}pass")

            return os.linesep.join(result)

        def mutate_function(self):
            tab = " " * 4
            field_names = list([x.name_snake for x in _.input_field_specs])

            result = [f"{tab}def mutate(self, {', '.join(['info'] + field_names)}):"]
            for item_posted in mutation.items_posted:
                item_name = item_posted.item_name
                result += [f"{tab}{tab}{item_name}_id = {item_name}_form.pop('id')"]
                result += [f"{tab}{tab}{u0(item_name)}.objects.update_or_create("]
                result += [f"{tab}{tab}{tab}id={item_name}_id,"]
                result += [f"{tab}{tab}{tab}defaults={item_name}_form"]
                result += [f"{tab}{tab})"]

            for item_posted in mutation.items_deleted:
                item_name = item_posted.item_name
                result += [f"{tab}{tab}{item_name} = {u0(item_name)}.objects.get("]
                for field_name in field_names:
                    result += [f"{tab}{tab}{tab}{field_name}={field_name},"]
                result += [f"{tab}{tab})"]
                result += [f"{tab}{tab}{item_name}.delete()", ""]

            result += [
                f"{tab}{tab}return {u0(mutation.name)}(success=True, errors={{}})"
            ]
            return os.linesep.join(result)

    return dict(sections=Sections(), _=_)


def render_mutation_endpoint(api_module, mutation, write_file, render_template):
    template_path = Path(__file__).parent / "templates"
    render_templates(template_path, get_context=lambda x: get_context(x, api_module))(
        mutation, write_file, render_template, output_path=api_module.merged_output_path
    )
