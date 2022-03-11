from typing import TYPE_CHECKING

from moonleap.typespec.recurse_type_specs import recurse_type_specs
from moonleap.utils.case import sn
from moonleap.utils.fp import uniq

if TYPE_CHECKING:
    from titan.django_pkg.module import Module


def find_module_that_provides_item_list(
    django_app, item_type_name, raise_if_not_found=True
) -> "Module":
    for module in django_app.modules:
        for item_list in module.item_lists_provided:
            if item_list.item_type.name == item_type_name:
                return module
    if raise_if_not_found:
        raise LookupError(f"Cannot find module that provides {item_type_name}")
    return None


def get_django_model_imports(django_app, type_specs):
    result = []
    for type_spec in type_specs:
        for field_spec in type_spec.get_field_specs(
            ["fk", "relatedSet", "form", "idList"]
        ):
            module = find_module_that_provides_item_list(django_app, field_spec.target)
            result.append(f"from {sn(module.name)}.models import {field_spec.target}")

    return uniq(result)


def get_graphene_type_imports(type_specs):
    queue = []
    for type_spec in type_specs:
        recurse_type_specs(type_spec, queue)

    result = []
    for type_spec in queue:
        for field_spec in type_spec.get_field_specs(["fk", "relatedSet", "form"]):
            tn_graphene = field_spec.target_type_spec.tn_graphene
            result.append(
                f"from api.types.{tn_graphene.lower()} "
                + f"import {tn_graphene}  # noqa"
            )

    return uniq(result)
