import ramda as R
from moonleap import u0


def find_module_that_provides_item_list(django_app, item_name):
    for module in django_app.modules:
        for item_list in module.item_lists_provided:
            if item_list.item_name == item_name:
                return module
    return None


def endpoint_imports_models(django_app, type_specs):
    result = []
    for type_spec in type_specs:
        for field_spec in type_spec.field_specs:
            if field_spec.field_type in ("fk", "related_set", "form"):
                item_name = field_spec.field_type_attrs["target"]
                module = find_module_that_provides_item_list(django_app, item_name)
                if module:
                    result.append(f"from {module.name}.models import {u0(item_name)}")

    return R.uniq(result)


def _recurse_type_specs(type_spec, result):
    if type_spec in result:
        return

    result.append(type_spec)
    for field_spec in type_spec.field_specs:
        if field_spec.fk_type_spec:
            _recurse_type_specs(field_spec.fk_type_spec, result)
    return result


def endpoint_imports_api(type_specs):
    queue = []
    for type_spec in type_specs:
        _recurse_type_specs(type_spec, queue)

    result = []
    for type_spec in queue:
        for field_spec in type_spec.field_specs:
            if field_spec.field_type in ("fk", "related_set", "form"):
                tn_graphene = field_spec.fk_type_spec.tn_graphene
                result.append(
                    f"from api.types.{tn_graphene.lower()} "
                    + f"import {tn_graphene}  # noqa"
                )

    return R.uniq(result)
