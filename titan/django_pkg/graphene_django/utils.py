from moonleap.resources.type_spec_store import type_spec_store
from moonleap.utils.case import lower0


def find_module_that_provides_item_list(django_app, item_name):
    for module in django_app.modules:
        for item_list in module.item_lists_provided:
            if item_list.item_name == item_name:
                return module
    return None


def endpoint_imports(django_app, item_names, field_spec):
    if field_spec.field_type in ("fk", "related_set"):
        item_name = lower0(field_spec.fk_type_spec.type_name)
        if item_name not in item_names:
            item_names.add(item_name)

            fk_type_spec = field_spec.fk_type_spec
            py_module_name = fk_type_spec.tn_graphene.lower()

            module = find_module_that_provides_item_list(django_app, item_name)
            return [
                f"from api.types.{py_module_name} "
                + f"import {fk_type_spec.tn_graphene}"
            ] + (
                [
                    f"from {module.name}.models import {fk_type_spec.tn_django_model}",
                ]
                if module
                else []
            )

    return []
