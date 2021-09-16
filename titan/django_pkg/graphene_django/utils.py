from moonleap.resources.type_spec_store import type_spec_store
from moonleap.utils.case import lower0


def field_arg_type(field_spec, args):
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


def find_module_that_provides_item_list(django_app, item_name):
    for module in django_app.modules:
        for item_list in module.item_lists_provided:
            if item_list.item_name == item_name:
                return module
    return None


def endpoint_imports(django_app, item_names, field_spec):
    if field_spec.field_type in ("fk", "list"):
        item_name = lower0(field_spec.fk_type_spec.type_name)
        if item_name not in item_names:
            item_names.add(item_name)

            module = find_module_that_provides_item_list(django_app, item_name)
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


def endpoint_args(field_spec_by_name):
    result = {}
    for field_name, field_spec in field_spec_by_name.items():
        result[field_name] = field_arg_type(field_spec, "")
    return result
