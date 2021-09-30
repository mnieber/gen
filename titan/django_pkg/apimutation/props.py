import os
from pathlib import Path

from moonleap import render_templates, u0
from moonleap.utils.magic_replace import magic_replace
from titan.django_pkg.graphene_django.utils import (
    endpoint_imports_api,
    endpoint_imports_models,
)


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


def _add_mutation_fields(fields, result):
    for field in fields:
        if field.field_type == "boolean":
            result.append(
                f'          {field.name}: {{"true" if {field.name_snake} else "false"}},'
            )
        else:
            result.append(f'          {field.name}: "{{{field.name_snake}}}",')


def _mutation_arguments(field_specs):
    result = {}
    for field_spec in field_specs:
        result[field_spec.name_snake] = graphene_type_from_field_spec(
            field_spec, f"required={field_spec.required}"
        )
    return result


def _default_value(field, item_name):
    t = field.field_type

    if t == "fk":
        return f"{field.name_snake}.id"

    if t == "boolean":
        return r"True"

    if t == "date":
        return r'"01-02-2003"'

    if t == "email":
        return r"email@email.com"

    if t == "slug":
        return r"foo-bar"

    if t == "uuid":
        return r'"41f55a14-a1b7-5697-84ef-c00e3f51c7e2"'

    if t == "string":
        return r'"foo"'

    if t == "url":
        return r'"https://foo.bar.com"'

    raise Exception(f"Unknown graphene field type: {t} in spec for {item_name}")


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
            type_specs = [_.inputs_type_spec, _.outputs_type_spec]
            result.extend(endpoint_imports_api(type_specs))
            result.extend(endpoint_imports_models(_.django_app, type_specs))

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

        def form_values(self):
            result = []
            indent = " " * 16

            for field in _.input_field_specs:
                if field.field_type == "form":
                    # form_type_spec = field.fk_type_spec
                    result.append(
                        f"{indent}{field.name_snake} = {field.name_snake}_form"
                    )
                else:
                    value = _default_value(field, mutation.name)
                    result.append(f"{indent}{field.name}={value}, ")

            return "\n".join(result)

        def create_mutation_function(self):
            result = []
            fields = [x for x in _.input_field_specs if not x.private]
            args = (", " if fields else "") + ", ".join([x.name_snake for x in fields])

            if True:
                result.append(
                    f"def create_red_rose_mutation(self{args}, output_values):"
                )
                result.append(r'  query = f"""')
                result.append(r"      mutation {{")
                result.append(r"        redRose(")
            _add_mutation_fields(fields, result)
            if True:
                result.append("        ) {{")
                result.append('          {", ".join(output_values)}')
                result.append("        }}")
                result.append("      }}")
                result.append('    """')
                result.append("  return query")

            return magic_replace(
                "\n".join(result),
                [
                    ("redRose", mutation.name),
                    ("red_rose", mutation.name_snake),
                ],
            )

    return dict(sections=Sections(), _=_)


def render_mutation_endpoint(api_module, mutation, write_file, render_template):
    template_path = Path(__file__).parent / "templates"
    render_templates(template_path, get_context=lambda x: get_context(x, api_module))(
        mutation, write_file, render_template, output_path=api_module.merged_output_path
    )
