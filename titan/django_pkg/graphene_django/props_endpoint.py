import os

from moonleap import upper0
from moonleap.resources.type_spec_store import type_spec_store
from moonleap.utils.case import lower0


def _field_arg_type(field_spec, args):
    if field_spec.field_type == "list":
        return f"graphene.List({field_spec.fk_type_spec.tn_graphene}{args})"

    if field_spec.field_type == "fk":
        return f"graphene.Field({field_spec.fk_type_spec.tn_graphene}{args})"

    if field_spec.field_type == "boolean":
        return f"graphene.Boolean()"

    if field_spec.field_type == "string":
        return f"graphene.String()"

    if field_spec.field_type == "any":
        return f"GenericScalar"

    return field_spec.field_type


def _return_value_for_field_spec(field_spec):
    if field_spec.field_type == "list":
        return f"{field_spec.fk_type_spec.tn_django_model}.objects.all()"

    if field_spec.field_type == "fk":
        return f"{field_spec.fk_type_spec.tn_django_model}.objects.all().first()"

    return "'hello'"


def _find_module_that_provides_item_list(django_app, item_name):
    for module in django_app.modules:
        for item_list in module.item_lists_provided:
            if item_list.item_name == item_name:
                return module
    return None


def _imports(django_app, item_names, field_spec):
    if field_spec.field_type in ("fk", "list"):
        item_name = lower0(field_spec.fk_type_spec.type_name)
        if item_name not in item_names:
            item_names.add(item_name)

            module = _find_module_that_provides_item_list(django_app, item_name)
            fk_type_spec = field_spec.fk_type_spec
            return [
                f"from api.types.{fk_type_spec.tn_graphene.lower()} "
                + f"import {fk_type_spec.tn_graphene}"
            ] + (
                [
                    f"from {module.name}.models import {fk_type_spec.tn_django_model}",
                ]
                if module
                else []
            )

    return []


def _args(field_spec_by_name):
    result = {}
    for field_name, field_spec in field_spec_by_name.items():
        result[field_name] = _field_arg_type(field_spec, "")
    return result


class SectionsQuery:
    def __init__(self, res):
        self.res = res

    def query_imports(self, query):
        result = []
        item_names = set()
        for (field_name, field_spec) in list(
            query.inputs_type_spec.field_spec_by_name.items()
        ) + list(query.outputs_type_spec.field_spec_by_name.items()):
            result.extend(_imports(self.res.service.django_app, item_names, field_spec))

        return os.linesep.join(result)

    def query_outputs(self, query):
        indent = " " * 4
        result = []

        for (
            field_name,
            field_spec,
        ) in query.outputs_type_spec.field_spec_by_name.items():
            args = ""
            result.append(f"{indent}{field_name} = {_field_arg_type(field_spec, args)}")

        return os.linesep.join(result)

    def query_resolve_functions(self, query):
        indent = " " * 4
        result = []

        for (
            field_name,
            field_spec,
        ) in query.outputs_type_spec.field_spec_by_name.items():
            result.append(f"{indent}def resolve_{field_name}():")
            result.append(
                f"{indent}  return {_return_value_for_field_spec(field_spec)}"
            )

        return os.linesep.join(result)


class SectionsMutation:
    def __init__(self, res):
        self.res = res

    def mutation_imports(self, mutation):
        result = []
        item_names = set()
        for (field_name, field_spec) in list(
            mutation.inputs_type_spec.field_spec_by_name.items()
        ) + list(mutation.outputs_type_spec.field_spec_by_name.items()):
            result.extend(_imports(self.res.service.django_app, item_names, field_spec))

        return os.linesep.join(result)

    def mutation_outputs(self, mutation):
        indent = " " * 4
        result = []

        for (
            field_name,
            field_spec,
        ) in mutation.outputs_type_spec.field_spec_by_name.items():
            args = ", ".join(
                f"{field_name}={arg}"
                for field_name, arg in _args(
                    mutation.inputs_type_spec.field_spec_by_name
                ).items()
            )
            result.append(f"{indent}{field_name} = {_field_arg_type(field_spec, args)}")

        return os.linesep.join(result)

    def mutation_arguments(self, mutation):
        indent = " " * 8
        result = []

        args = _args(mutation.inputs_type_spec.field_spec_by_name)
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
