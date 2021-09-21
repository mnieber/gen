import os

from moonleap import upper0
from moonleap.resources.type_spec_store import type_spec_store
from titan.django_pkg.graphene_django.utils import endpoint_imports


def mutation_argument_type(field_spec, args):
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
        result[field_spec.name_snake] = mutation_argument_type(
            field_spec, f"required={field_spec.required}"
        )
    return result


class SectionsMutation:
    def __init__(self, res):
        self.res = res

    def mutation_imports(self, mutation):
        result = []
        item_names = set()
        for field_spec in list(mutation.inputs_type_spec.field_specs) + list(
            mutation.outputs_type_spec.field_specs
        ):
            result.extend(
                endpoint_imports(self.res.service.django_app, item_names, field_spec)
            )

        return os.linesep.join(result)

    def mutation_outputs(self, mutation):
        indent = " " * 4
        result = []

        for field_spec in mutation.outputs_type_spec.field_specs:
            args = ""
            result.append(
                f"{indent}{field_spec.name} = {mutation_argument_type(field_spec, args)}"
            )

        return os.linesep.join(result)

    def mutation_arguments(self, mutation):
        indent = " " * 8
        result = []

        args = _mutation_arguments(mutation.inputs_type_spec.field_specs)
        for field_name, arg in args.items():
            result.append(f"{indent}{field_name} = {arg}")
        if not args:
            result.append(f"{indent}pass")

        return os.linesep.join(result)

    def mutate_function(self, mutation):
        tab = " " * 4
        field_names = list(
            [x.name_snake for x in mutation.inputs_type_spec.field_specs]
        )

        result = [f"{tab}def mutate(self, {', '.join(['info'] + field_names)}):"]
        for item_posted in mutation.items_posted:
            item_name = item_posted.item_name
            result += [f"{tab}{tab}{item_name} = {upper0(item_name)}("]
            for field_name in field_names:
                result += [f"{tab}{tab}{tab}{field_name}={field_name},"]
            result += [f"{tab}{tab})"]
            result += [f"{tab}{tab}{item_name}.save()", ""]

        for item_posted in mutation.items_deleted:
            item_name = item_posted.item_name
            result += [f"{tab}{tab}{item_name} = {upper0(item_name)}.objects.get("]
            for field_name in field_names:
                result += [f"{tab}{tab}{tab}{field_name}={field_name},"]
            result += [f"{tab}{tab})"]
            result += [f"{tab}{tab}{item_name}.delete()", ""]

        result += [
            f"{tab}{tab}return {upper0(mutation.name)}(success=True, errors={{}})"
        ]
        return os.linesep.join(result)
