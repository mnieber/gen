import ramda as R
from moonleap import u0
from moonleap.typespec.recurse_type_specs import recurse_type_specs


def find_module_that_provides_item_list(django_app, item_name):
    for module in django_app.modules:
        for item_list in module.item_lists_provided:
            if item_list.item_name == item_name:
                return module
    raise Exception(f"Cannot find module that provides {item_name}")


def get_django_model_imports(django_app, type_specs):
    result = []
    for type_spec in type_specs:
        for field_spec in type_spec.get_field_specs(["fk", "relatedSet", "form"]):
            item_name = field_spec.target
            module = find_module_that_provides_item_list(django_app, item_name)
            result.append(f"from {module.name}.models import {u0(item_name)}")

    return R.uniq(result)


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

    return R.uniq(result)
