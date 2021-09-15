import os

from moonleap.utils.case import lower0


def _field_arg_type(field_spec):
    if field_spec.field_type == "list":
        return f"graphene.List({field_spec.field_type_attrs['target']}Type)"

    if field_spec.field_type == "fk":
        return f"graphene.Field({field_spec.field_type_attrs['target']}Type)"

    return field_spec.field_type


def _return_value_for_field_spec(field_spec):
    if field_spec.field_type == "list":
        return f"{field_spec.field_type_attrs['target']}.objects.all()"

    if field_spec.field_type == "fk":
        return f"{field_spec.field_type_attrs['target']}.objects.all().first()"

    return "'hello'"


def _find_module_that_provides_item_list(django_app, item_name):
    for module in django_app.modules:
        for item_list in module.item_lists_provided:
            if item_list.item_name == item_name:
                return module
    return None


def _imports(django_app, datatypes, field_spec):
    if field_spec.field_type in ("fk", "list"):
        datatype = field_spec.field_type_attrs["target"]
        if datatype not in datatypes:
            datatypes.add(datatype)
            module = _find_module_that_provides_item_list(django_app, lower0(datatype))
            return [f"from api.types.{datatype.lower()}type import {datatype}Type"] + (
                [
                    f"from {module.name}.models import {datatype}",
                ]
                if module
                else []
            )

    return []


class SectionsQuery:
    def __init__(self, res):
        self.res = res

    def query_imports(self, query):
        result = []
        datatypes = set()
        for (field_name, field_spec) in list(
            query.inputs_type_spec.field_spec_by_name.items()
        ) + list(query.outputs_type_spec.field_spec_by_name.items()):
            result.extend(_imports(self.res.service.django_app, datatypes, field_spec))

        return os.linesep.join(result)

    def query_outputs(self, query):
        indent = " " * 4
        result = []

        for (
            field_name,
            field_spec,
        ) in query.outputs_type_spec.field_spec_by_name.items():
            result.append(f"{indent}{field_name} = {_field_arg_type(field_spec)}")

        return os.linesep.join(result)

    def query_arguments(self, query):
        indent = " " * 8
        result = []

        for field_name, field_spec in query.inputs_type_spec.field_spec_by_name.items():
            result.append(f"{indent}{field_name} = graphene.String()")
        else:
            result.append(f"{indent}pass")

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
