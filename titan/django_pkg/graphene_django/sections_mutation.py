import os

from moonleap import upper0
from moonleap.resources.type_spec_store import type_spec_store
from titan.django_pkg.graphene_django.utils import (
    endpoint_args,
    endpoint_imports,
    field_arg_type,
)


class SectionsMutation:
    def __init__(self, res):
        self.res = res

    def mutation_imports(self, mutation):
        result = []
        item_names = set()
        for (field_name, field_spec) in list(
            mutation.inputs_type_spec.field_spec_by_name.items()
        ) + list(mutation.outputs_type_spec.field_spec_by_name.items()):
            result.extend(
                endpoint_imports(self.res.service.django_app, item_names, field_spec)
            )

        return os.linesep.join(result)

    def mutation_outputs(self, mutation):
        indent = " " * 4
        result = []

        for (
            field_name,
            field_spec,
        ) in mutation.outputs_type_spec.field_spec_by_name.items():
            args = ""
            result.append(f"{indent}{field_name} = {field_arg_type(field_spec, args)}")

        return os.linesep.join(result)

    def mutation_arguments(self, mutation):
        indent = " " * 8
        result = []

        args = endpoint_args(mutation.inputs_type_spec.field_spec_by_name)
        for field_name, arg in args.items():
            result.append(f"{indent}{field_name} = {arg}")
        if not args:
            result.append(f"{indent}pass")

        return os.linesep.join(result)

    def mutate_function(self, mutation):
        tab = " " * 4
        field_names = list(mutation.inputs_type_spec.field_spec_by_name.keys())

        result = [f"{tab}def mutate(self, {', '.join(['info'] + field_names)}):"]
        for item_posted in mutation.items_posted:
            item_name = item_posted.item_name
            type_spec = type_spec_store.get(item_name)
            result += [f"{tab}{tab}{item_name} = {type_spec.tn_django_model}("]
            for field_name in field_names:
                result += [f"{tab}{tab}{tab}{field_name}={field_name},"]
            result += [f"{tab}{tab})"]
            result += [f"{tab}{tab}{item_name}.save()", ""]

        for item_posted in mutation.items_deleted:
            item_name = item_posted.item_name
            type_spec = type_spec_store.get(item_name)
            result += [
                f"{tab}{tab}{item_name} = {type_spec.tn_django_model}.objects.get("
            ]
            for field_name in field_names:
                result += [f"{tab}{tab}{tab}{field_name}={field_name},"]
            result += [f"{tab}{tab})"]
            result += [f"{tab}{tab}{item_name}.delete()", ""]

        result += [
            f"{tab}{tab}return {upper0(mutation.name)}(success=True, errors={{}})"
        ]
        return os.linesep.join(result)
